import random

from combat.combat_constants import (
    ACTION_ACT,
    ACTION_BLOCK,
    ACTION_DODGE,
    ACTION_FIGHT,
    ACTION_ITEM,
    ACTION_NP,
    AI_NP_THRESHOLD,
    BLOCK_DAMAGE_REDUCTION,
    AI_SKILL_CHANCE,
    CRIT_CHANCE_BASE,
    EXHAUSTION_THRESHOLD,
    HP_REGEN_DEFAULT,
    MANA_REGEN_DEFAULT,
    MANA_REGEN_REST,
    NP_COST_DEFAULT,
    NP_GAIN_ON_HIT,
    NP_GAIN_ON_HIT_RECV,
    NP_MAX,
    SP_COST_BLOCK,
    SP_REGEN_CONSECUTIVE,
    SP_REGEN_IDLE,
    SP_REGEN_REST,
)
from combat.combat_result import CombatResult
from combat.damage_calc import calculate_damage
from combat.dodge_calc import attempt_dodge
from combat.item_data import DEFAULT_INVENTORY, ITEMS
from combat.passive_triggers import (
    HOOK_ON_DEATH,
    HOOK_ON_DODGE_FAIL,
    HOOK_ON_DODGE_SUC,
    HOOK_ON_HIT,
    HOOK_ON_HIT_RECV,
    HOOK_ON_LOW_HP,
    HOOK_ON_LOW_SP,
    HOOK_ON_NP_USE,
    HOOK_ON_SKILL_USE,
    fire_hook,
)
from combat.status_effects import tick_statuses


def initialize_runtime_state(state):
    ctx = state.context_flags
    ctx.setdefault("player_np", 0)
    ctx.setdefault("enemy_np", 0)
    ctx.setdefault("player_cooldowns", {})
    ctx.setdefault("enemy_cooldowns", {})
    ctx.setdefault("player_skill_uses", {})
    ctx.setdefault("enemy_skill_uses", {})
    ctx.setdefault("inventory", list(DEFAULT_INVENTORY))
    ctx.setdefault("result_flags", set())
    ctx.setdefault("effect_turns", {})
    ctx.setdefault("effect_values", {})
    ctx.setdefault("total_dodge_attempts", 0)
    ctx.setdefault("low_hp_triggered", False)
    ctx.setdefault("low_sp_triggered", False)
    ctx.setdefault("used_np_this_battle", False)
    ctx.setdefault("auto_dodge_intent", False)
    ctx.setdefault("player_blocking", False)
    ctx.setdefault("pending_enemy_action", None)
    ctx.setdefault("turn_skill_cooldown_log", [])
    ctx.setdefault("turn_action_label", None)

    if "turn_flags" not in ctx:
        _reset_turn_flags(state)


def process_player_action(state, selected_action):
    initialize_runtime_state(state)
    action_payload = _normalize_action_payload(selected_action)
    action = action_payload.get("action")

    if action not in {ACTION_FIGHT, ACTION_ACT, ACTION_ITEM, ACTION_NP, ACTION_DODGE, ACTION_BLOCK}:
        return None

    committed = False

    if action == ACTION_FIGHT:
        committed = _perform_player_attack(state, source_label="FIGHT", damage_mult=1.0)

    elif action == ACTION_ACT:
        committed = _execute_player_skill(state, action_payload.get("skill_id"))

    elif action == ACTION_ITEM:
        committed = _use_item(state, action_payload.get("item_id"))

    elif action == ACTION_NP:
        committed = _execute_player_np(state, action_payload.get("mode", "base"))

    elif action == ACTION_DODGE:
        state.context_flags["auto_dodge_intent"] = True
        state.context_flags["turn_action_label"] = "DODGE"
        state.context_flags["turn_flags"]["rested"] = True
        state.log_event("You hold position and prepare to evade the next strike.")
        committed = True

    elif action == ACTION_BLOCK:
        committed = _prepare_block(state)

    if not committed:
        return None

    if state.enemy.hp <= 0:
        return _build_result(state, "player")

    state.phase = "enemy_attack"
    return None


def process_enemy_turn(state):
    initialize_runtime_state(state)

    if state.phase == "enemy_attack":
        pending = _prepare_enemy_action(state)
        state.context_flags["pending_enemy_action"] = pending
        state.phase = "dodge_phase"
        state.log_event(pending["announce"])

        if state.context_flags.pop("auto_dodge_intent", False):
            state.context_flags["dodge_choice"] = True

        if (
            state.player.name == "Stella"
            and state.player.passives.get("cautious_step")
            and not state.player.unique_vars.get("first_attack_auto_dodge_used", False)
            and state.turn == 0
        ):
            state.player.unique_vars["first_attack_auto_dodge_used"] = True
            state.context_flags["dodge_choice"] = True
            state.log_event("Cautious Step triggers an automatic dodge attempt.")
        return None

    if state.phase != "dodge_phase":
        return None

    if "dodge_choice" not in state.context_flags and not state.context_flags.get("player_blocking", False):
        return None

    pending = state.context_flags.pop("pending_enemy_action", None)
    has_dodge_choice = "dodge_choice" in state.context_flags
    dodge_choice = bool(state.context_flags.pop("dodge_choice", False))
    if pending is None:
        state.phase = "player_action"
        return None

    turn_flags = state.context_flags["turn_flags"]
    turn_flags["attempted_dodge"] = has_dodge_choice and dodge_choice

    if has_dodge_choice and dodge_choice:
        state.context_flags["total_dodge_attempts"] += 1
        success, _ = _resolve_dodge_attempt(state)
        if success:
            turn_flags["dodge_success"] = True
            state.consecutive_dodges += 1
            fire_hook(HOOK_ON_DODGE_SUC, state, state.player.name, {"turn": state.turn})
            state.log_event(f"Dodge success - {pending['label']} misses cleanly.")
        else:
            state.consecutive_dodges = 0
            fire_hook(HOOK_ON_DODGE_FAIL, state, state.player.name, {"turn": state.turn})
            _enemy_hits_player(state, pending["damage"], pending["label"])

    elif state.context_flags.pop("player_blocking", False):
        if state.player.sp >= SP_COST_BLOCK:
            state.player.sp = max(0, state.player.sp - SP_COST_BLOCK)

            reduced = max(1, int(pending["damage"] * BLOCK_DAMAGE_REDUCTION))
            absorbed = pending["damage"] - reduced

            turn_flags["blocked"] = True
            state.consecutive_dodges = 0

            _enemy_hits_player(state, reduced, pending["label"] + " (blocked)")
            state.log_event(f"Block absorbs {absorbed} damage.")

        else:
            state.log_event("Stance collapses -- insufficient SP.")
            state.consecutive_dodges = 0
            _enemy_hits_player(state, pending["damage"], pending["label"])

    else:
        state.consecutive_dodges = 0
        _enemy_hits_player(state, pending["damage"], pending["label"])

    result = _resolve_player_death(state)
    if result:
        _append_turn_skill_cooldown_log(state)
        return result

    tick_statuses(state.player_statuses, state.player, state)
    tick_statuses(state.enemy_statuses, state.enemy, state)

    _apply_end_turn_recovery(state)
    _tick_cooldowns(state.context_flags["player_cooldowns"])
    _tick_cooldowns(state.context_flags["enemy_cooldowns"])
    _tick_effects(state)
    _check_threshold_hooks(state)
    _append_turn_skill_cooldown_log(state)

    if state.enemy.hp <= 0:
        return _build_result(state, "player")

    _reset_turn_flags(state)
    state.phase = "player_action"
    return None


def _normalize_action_payload(selected_action):
    if isinstance(selected_action, dict):
        return selected_action
    return {"action": selected_action}


def _perform_player_attack(state, source_label: str, damage_mult: float):
    if not state.context_flags.get("turn_action_label"):
        state.context_flags["turn_action_label"] = source_label

    state.context_flags["turn_flags"]["rested"] = False

    sure_hit = bool(state.context_flags.pop("player_next_hit_sure", False))
    force_crit = bool(state.context_flags.pop("player_next_hit_crit", False))
    crit_chance = 1.0 if force_crit else CRIT_CHANCE_BASE

    if not sure_hit and random.random() < max(0.0, min(0.35, state.enemy.base_dodge * 0.35)):
        state.log_event(f"{state.player.name}'s attack misses.")
        return True

    final_mult = damage_mult * _player_damage_multiplier(state)
    damage, is_crit = calculate_damage(
        attack=state.player.base_attack,
        defense_factor=_enemy_defense_factor(state),
        damage_multiplier=final_mult,
        crit_chance=crit_chance,
    )
    _player_hits_enemy(state, damage, source_label, is_crit)
    return True


def _execute_player_skill(state, skill_id):
    if not skill_id:
        state.log_event("Choose a skill from the ACT submenu.")
        return False

    skill = _find_skill(state.player.actives, skill_id)
    if skill is None:
        state.log_event("Skill not found.")
        return False

    cooldowns = state.context_flags["player_cooldowns"]
    uses = state.context_flags["player_skill_uses"]

    if not _is_skill_available(state.player, skill, cooldowns, uses):
        state.log_event(f"{skill['name']} is unavailable.")
        return False

    mana_cost = _skill_mana_cost(skill, uses)
    if state.player.mana < mana_cost:
        state.log_event("Not enough mana.")
        return False

    state.player.mana -= mana_cost
    _register_skill_use(skill, cooldowns, uses)
    state.context_flags["turn_action_label"] = skill["name"]
    state.context_flags["turn_flags"]["used_skill"] = True
    state.context_flags["turn_flags"]["rested"] = False

    fire_hook(HOOK_ON_SKILL_USE, state, state.player.name, {"skill_id": skill_id})
    state.log_event(f"{state.player.name} uses {skill['name']}.")

    _apply_skill_effect(state, skill)

    skill_damage_mult = float(skill.get("damage_mult", 1.0))
    if skill.get("id") == "zuxi_combat_call" and state.context_flags.get("zuxi_true_name_empower", False):
        skill_damage_mult *= 1.5

    if skill.get("damage_mult"):
        _perform_player_attack(
            state,
            source_label=skill["name"],
            damage_mult=skill_damage_mult,
        )

    return True


def _use_item(state, item_id):
    if not item_id:
        state.log_event("Choose an item from the ITEM submenu.")
        return False

    inventory = state.context_flags.get("inventory", [])
    if item_id not in inventory:
        state.log_event("That item is not in your inventory.")
        return False

    item = ITEMS.get(item_id)
    if item is None:
        state.log_event("Item data is missing.")
        return False

    inventory.remove(item_id)
    state.context_flags["turn_action_label"] = item["name"]
    state.context_flags["turn_flags"]["rested"] = True

    category = item.get("category")
    restore = int(item.get("restore", 0))

    if category == "hp":
        state.player.hp = min(state.player.hp_max, state.player.hp + restore)
    elif category == "sp":
        state.player.sp = min(state.player.sp_max, state.player.sp + restore)
    elif category == "mana":
        state.player.mana = min(state.player.mana_max, state.player.mana + restore)

    state.log_event(f"Used {item['name']}.")
    return True


def _execute_player_np(state, mode: str):
    np_item = state.player.np_item or {}
    if not np_item:
        state.log_event("No Noble Phantasm equipped.")
        return False

    if state.context_flags.get("player_np", 0) < NP_COST_DEFAULT:
        state.log_event("NP gauge is not full.")
        return False

    true_name = mode == "true_name"
    mana_cost = np_item.get("true_name_cost") if true_name else np_item.get("base_mana_cost", 50)

    once_per_battle = bool(np_item.get("once_per_battle"))
    if true_name and once_per_battle and state.context_flags.get("np_true_name_used", False):
        state.log_event("True Name Release already used this battle.")
        return False

    if state.player.mana < mana_cost:
        state.log_event("Not enough mana for Noble Phantasm.")
        return False

    state.player.mana -= mana_cost
    state.context_flags["player_np"] = 0
    state.context_flags["turn_action_label"] = "NP True Name" if true_name else "NP"
    state.context_flags["used_np_this_battle"] = True
    state.context_flags["result_flags"].add("used_np")
    state.context_flags["turn_flags"]["used_np"] = True
    state.context_flags["turn_flags"]["rested"] = False

    # NP release instantly refreshes Combat Call if it is cooling down.
    player_cooldowns = state.context_flags.get("player_cooldowns", {})
    if int(player_cooldowns.get("zuxi_combat_call", 0)) > 0:
        player_cooldowns.pop("zuxi_combat_call", None)
        state.log_event("Zuxi - Combat Call is instantly refreshed.")

    if true_name:
        state.context_flags["np_true_name_used"] = True
        state.context_flags["zuxi_true_name_empower"] = True
        state.log_event("True Name resonance empowers Zuxi - Combat Call by 50%.")

    fire_hook(HOOK_ON_NP_USE, state, state.player.name, {"mode": mode})

    mult = 3.0 if true_name else 2.2
    defense_factor = 1.0 if true_name else _enemy_defense_factor(state)
    damage, _ = calculate_damage(
        attack=state.player.base_attack,
        defense_factor=defense_factor,
        damage_multiplier=mult * _player_damage_multiplier(state),
        crit_chance=0.0,
    )
    _player_hits_enemy(state, damage, np_item.get("name", "Noble Phantasm"), is_crit=False)
    return True


def _apply_skill_effect(state, skill):
    effect = skill.get("effect")
    if not effect:
        return

    if effect == "mana_burst":
        # Mana Burst becomes a timed explosive-wave attack mode.
        _set_effect(state, "mana_burst_wave", 3)
        state.log_event("Mana Burst forms an explosive wave for 3 turns.")
    elif effect == "guaranteed_dodge":
        state.context_flags["player_next_dodge_guaranteed"] = True
    elif effect == "clear_fear":
        state.player.unique_vars["emotional_severance_turns"] = 2
    elif effect == "zero_state":
        state.player.unique_vars["zero_state_active"] = True
        state.player.passives["minds_eye"] = False
        state.player.hp = min(state.player.hp_max, state.player.hp + int(state.player.hp_max * 0.30))
        _set_effect(state, "sp_cost_half", 3)
    elif effect == "enemy_damage_down":
        _set_effect(state, "enemy_damage_down_25", 3)
    elif effect == "reveal_and_dodge_boost":
        state.context_flags["enemy_next_attack_revealed"] = True
        _set_effect(state, "player_dodge_up_20", 1)
    elif effect == "territory_field":
        state.player.unique_vars["territory_active"] = True
        state.player.unique_vars["territory_turns"] = 5
        _set_effect(state, "territory_creation", 5)
    elif effect == "cleanse_and_sp_restore":
        state.player_statuses.clear()
        state.player.sp = min(state.player.sp_max, state.player.sp + 15)
    elif effect == "sure_hit_next":
        state.context_flags["player_next_hit_sure"] = True
    elif effect == "emergency_heal":
        threshold = int(state.player.hp_max * 0.20)
        heal_pct = 0.40 if state.player.hp <= threshold else 0.20
        state.player.hp = min(state.player.hp_max, state.player.hp + int(state.player.hp_max * heal_pct))
    elif effect == "target_defense_down":
        _set_effect(state, "enemy_def_down_20", 3)
    elif effect == "damage_down_dodge_up":
        _set_effect(state, "enemy_damage_down_30", 2)
        _set_effect(state, "player_dodge_up_15", 2)
    elif effect == "summon_spirit":
        _set_effect(state, "player_damage_up_10", 3)
    elif effect == "iron_path_mode":
        state.player.unique_vars["iron_path_active"] = True
        _set_effect(state, "player_dodge_up_20", 2)
        _set_effect(state, "player_damage_up_05", 3)
    elif effect == "next_attack_amp":
        state.context_flags["player_next_damage_amp"] = max(
            1.5,
            float(state.context_flags.get("player_next_damage_amp", 1.0)),
        )
    elif effect == "guaranteed_crit_next":
        state.context_flags["player_next_hit_crit"] = True
    elif effect == "instant_profile":
        state.player.unique_vars["profile_complete"] = True
        _set_effect(state, "player_dodge_up_20", 2)
    elif effect == "permanent_enemy_stat_down":
        _set_effect(state, "enemy_stat_down_20", 99)
    elif effect == "rage_mode":
        _set_effect(state, "player_damage_up_30", 2)
        _set_effect(state, "player_dodge_down_10", 2)
    elif effect == "pattern_analysis":
        _set_effect(state, "player_dodge_up_15", 3)
    elif effect == "copy_enemy_skill":
        _set_effect(state, "player_damage_up_10", 3)
    elif effect == "heavy_hit_stun_self":
        _set_effect(state, "self_stunned", 1)


def _prepare_enemy_action(state):
    enemy = state.enemy
    enemy_cooldowns = state.context_flags["enemy_cooldowns"]
    enemy_uses = state.context_flags["enemy_skill_uses"]

    if (
        state.context_flags.get("enemy_np", 0) >= AI_NP_THRESHOLD
        and enemy.np_item
        and enemy.mana >= enemy.np_item.get("base_mana_cost", 50)
    ):
        mana_cost = int(enemy.np_item.get("base_mana_cost", 50))
        enemy.mana -= mana_cost
        state.context_flags["enemy_np"] = 0
        damage, _ = calculate_damage(
            attack=enemy.base_attack,
            defense_factor=1.0,
            damage_multiplier=2.1 * _enemy_damage_multiplier(state),
            crit_chance=0.05,
        )
        return {
            "label": enemy.np_item.get("name", "Noble Phantasm"),
            "damage": damage,
            "announce": f"{enemy.name} invokes {enemy.np_item.get('name', 'Noble Phantasm')}!",
        }

    available_skills = [
        skill
        for skill in enemy.actives
        if _is_skill_available(enemy, skill, enemy_cooldowns, enemy_uses)
    ]

    if available_skills and random.random() < AI_SKILL_CHANCE:
        skill = random.choice(available_skills)
        mana_cost = _skill_mana_cost(skill, enemy_uses)
        enemy.mana -= mana_cost
        _register_skill_use(skill, enemy_cooldowns, enemy_uses)

        damage_mult = float(skill.get("damage_mult", 1.2))
        damage, _ = calculate_damage(
            attack=enemy.base_attack,
            defense_factor=1.0,
            damage_multiplier=damage_mult * _enemy_damage_multiplier(state),
            crit_chance=CRIT_CHANCE_BASE,
        )
        return {
            "label": skill["name"],
            "damage": damage,
            "announce": f"{enemy.name} prepares {skill['name']}.",
        }

    damage, is_crit = calculate_damage(
        attack=enemy.base_attack,
        defense_factor=1.0,
        damage_multiplier=_enemy_damage_multiplier(state),
        crit_chance=CRIT_CHANCE_BASE,
    )
    crit_text = " (critical)" if is_crit else ""
    return {
        "label": "basic attack",
        "damage": damage,
        "announce": f"{enemy.name} lunges with a basic attack{crit_text}.",
    }


def _resolve_dodge_attempt(state):
    if _has_effect(state, "self_stunned"):
        state.log_event("You are stunned and fail to react.")
        return False, 0

    if state.context_flags.pop("player_next_dodge_guaranteed", False):
        return True, 0

    if state.player.passives.get("minds_eye") and not state.player.unique_vars.get("minds_eye_free_dodge_used", False):
        state.player.unique_vars["minds_eye_free_dodge_used"] = True
        return True, 0

    dodge_bonus = _player_dodge_bonus(state)
    if dodge_bonus:
        state.player.base_dodge = max(0.0, state.player.base_dodge + dodge_bonus)

    perfected = bool(state.player.passives.get("perfected_form"))
    success, sp_cost = attempt_dodge(
        state.player,
        state.consecutive_dodges,
        perfected_form=perfected,
    )

    if dodge_bonus:
        state.player.base_dodge = max(0.0, state.player.base_dodge - dodge_bonus)

    if success:
        if _has_effect(state, "sp_cost_half"):
            sp_cost = max(1, sp_cost // 2)
        state.player.sp = max(0, state.player.sp - sp_cost)

    return success, sp_cost


def _player_hits_enemy(state, damage: int, source_label: str, is_crit: bool):
    state.enemy.hp = max(0, state.enemy.hp - damage)
    crit_text = " (CRIT)" if is_crit else ""
    state.log_event(f"{state.player.name} uses {source_label} for {damage} damage{crit_text}.")

    state.context_flags["player_np"] = min(NP_MAX, state.context_flags["player_np"] + NP_GAIN_ON_HIT)
    state.context_flags["enemy_np"] = min(NP_MAX, state.context_flags["enemy_np"] + NP_GAIN_ON_HIT_RECV)
    fire_hook(HOOK_ON_HIT, state, state.player.name, {"damage": damage})


def _enemy_hits_player(state, damage: int, source_label: str):
    resistance = max(0.0, float(state.player.unique_vars.get("damage_resistance_bonus", 0.0)))
    damage = max(1, int(round(damage * (1.0 - resistance))))

    state.player.hp = max(0, state.player.hp - damage)
    state.log_event(f"{state.enemy.name}'s {source_label} deals {damage} damage.")

    state.context_flags["enemy_np"] = min(NP_MAX, state.context_flags["enemy_np"] + NP_GAIN_ON_HIT)
    state.context_flags["player_np"] = min(NP_MAX, state.context_flags["player_np"] + NP_GAIN_ON_HIT_RECV)
    fire_hook(HOOK_ON_HIT_RECV, state, state.player.name, {"damage": damage})


def _resolve_player_death(state):
    if state.player.hp > 0:
        return None

    fire_hook(HOOK_ON_DEATH, state, state.player.name, {"turn": state.turn})
    if state.player.hp > 0:
        return None

    return _build_result(state, "enemy")


def _build_result(state, winner: str):
    flags = set(state.context_flags.get("result_flags", set()))

    if state.context_flags.get("used_np_this_battle", False):
        flags.add("used_np")

    if winner == "player" and state.context_flags.get("spirit_hunt", False):
        flags.add("spirit_captured")

    if winner == "player" and state.context_flags.get("total_dodge_attempts", 0) == 0:
        flags.add("survived_without_dodge")

    if state.player.hp <= int(state.player.hp_max * 0.5):
        flags.add("below_half_hp")

    return CombatResult(
        winner=winner,
        hp_remaining=state.player.hp,
        sp_remaining=state.player.sp,
        mana_remaining=state.player.mana,
        turns_taken=state.turn,
        flags=sorted(flags),
    )


def _apply_end_turn_recovery(state):
    flags = state.context_flags["turn_flags"]

    if flags["attempted_dodge"] and flags["dodge_success"]:
        regen_sp = 0

    elif flags["attempted_dodge"] and not flags["dodge_success"]:
        regen_sp = SP_REGEN_CONSECUTIVE if state.consecutive_dodges > 1 else 3

    elif flags.get("blocked"):
        regen_sp = 5

    else:
        regen_sp = SP_REGEN_REST if flags["rested"] else SP_REGEN_IDLE

    state.player.sp = min(state.player.sp_max, state.player.sp + regen_sp)

    if state.player.name == "Atrox":
        if state.player.sp < int(state.player.sp_max * 0.30):
            state.player.sp = min(state.player.sp_max, state.player.sp + 10)
        if state.player.hp < int(state.player.hp_max * 0.20):
            state.player.hp = min(state.player.hp_max, state.player.hp + int(state.player.hp_max * 0.05))

    mana_regen = MANA_REGEN_DEFAULT if (flags["used_skill"] or flags["used_np"]) else MANA_REGEN_REST
    state.player.mana = min(state.player.mana_max, state.player.mana + mana_regen)

    if HP_REGEN_DEFAULT > 0:
        state.player.hp = min(state.player.hp_max, state.player.hp + HP_REGEN_DEFAULT)


def _check_threshold_hooks(state):
    if not state.context_flags.get("low_hp_triggered", False) and state.player.hp < int(state.player.hp_max * 0.30):
        fire_hook(HOOK_ON_LOW_HP, state, state.player.name, {"turn": state.turn})
        state.context_flags["low_hp_triggered"] = True

    if not state.context_flags.get("low_sp_triggered", False) and state.player.sp < EXHAUSTION_THRESHOLD:
        fire_hook(HOOK_ON_LOW_SP, state, state.player.name, {"turn": state.turn})
        state.context_flags["low_sp_triggered"] = True


def _enemy_defense_factor(state):
    factor = 1.0

    if state.player.name == "Atrox":
        stacks = int(state.player.unique_vars.get("defense_debuff_stacks", 0))
        factor *= max(0.5, 1.0 - (0.05 * stacks))

    if _has_effect(state, "enemy_def_down_20"):
        factor *= 0.80

    if _has_effect(state, "enemy_stat_down_20"):
        factor *= 0.80

    return max(0.30, factor)


def _player_damage_multiplier(state):
    mult = 1.0
    mult += float(state.player.unique_vars.get("song_bonus", 0.0))
    mult += float(state.player.unique_vars.get("rage_damage_bonus", 0.0))

    if _has_effect(state, "mana_burst_wave"):
        mult += 0.15
    if _has_effect(state, "territory_creation"):
        mult += 0.10
    if _has_effect(state, "player_damage_up_05"):
        mult += 0.05
    if _has_effect(state, "player_damage_up_10"):
        mult += 0.10
    if _has_effect(state, "player_damage_up_30"):
        mult += 0.30

    mult *= float(state.context_flags.pop("player_next_damage_amp", 1.0))
    return max(0.1, mult)


def _enemy_damage_multiplier(state):
    mult = 1.0
    if _has_effect(state, "enemy_damage_down_25"):
        mult *= 0.75
    if _has_effect(state, "enemy_damage_down_30"):
        mult *= 0.70
    if _has_effect(state, "enemy_stat_down_20"):
        mult *= 0.80
    return max(0.1, mult)


def _player_dodge_bonus(state):
    bonus = 0.0
    if _has_effect(state, "territory_creation"):
        bonus += 0.10
    if _has_effect(state, "player_dodge_up_10"):
        bonus += 0.10
    if _has_effect(state, "player_dodge_up_15"):
        bonus += 0.15
    if _has_effect(state, "player_dodge_up_20"):
        bonus += 0.20
    if _has_effect(state, "player_dodge_down_10"):
        bonus -= 0.10
    if _has_effect(state, "player_dodge_down_15"):
        bonus -= 0.15

    if state.player.name == "Kiki" and state.context_flags.get("enemy_next_attack_revealed", False):
        bonus += 0.10

    return bonus


def _set_effect(state, key: str, turns: int, value=1):
    effect_turns = state.context_flags["effect_turns"]
    effect_values = state.context_flags["effect_values"]
    effect_turns[key] = max(turns, int(effect_turns.get(key, 0)))
    effect_values[key] = value


def _has_effect(state, key: str) -> bool:
    return int(state.context_flags["effect_turns"].get(key, 0)) > 0


def _tick_effects(state):
    effect_turns = state.context_flags["effect_turns"]
    effect_values = state.context_flags["effect_values"]

    for key in list(effect_turns.keys()):
        effect_turns[key] -= 1
        if effect_turns[key] <= 0:
            effect_turns.pop(key, None)
            effect_values.pop(key, None)


def _is_skill_available(owner, skill, cooldowns, uses):
    skill_id = skill.get("id")
    if not skill_id:
        return False

    if owner.name == "Nasir" and skill_id == "adaptive_activate" and owner.unique_vars.get("adaptive_locked", False):
        return False

    if int(cooldowns.get(skill_id, 0)) > 0:
        return False

    limit = skill.get("uses")
    if limit is not None and int(uses.get(skill_id, 0)) >= int(limit):
        return False

    return owner.mana >= _skill_mana_cost(skill, uses)


def _skill_mana_cost(skill, uses):
    cost = int(skill.get("mana_cost", 0))
    if skill.get("id") == "mana_burst":
        cost += 5 * int(uses.get("mana_burst", 0))
    return cost


def _register_skill_use(skill, cooldowns, uses):
    skill_id = skill.get("id")
    uses[skill_id] = int(uses.get(skill_id, 0)) + 1

    cooldown = skill.get("cooldown")
    if isinstance(cooldown, int) and cooldown > 0:
        cooldowns[skill_id] = cooldown


def _tick_cooldowns(cooldowns):
    for skill_id in list(cooldowns.keys()):
        cooldowns[skill_id] = int(cooldowns[skill_id]) - 1
        if cooldowns[skill_id] <= 0:
            cooldowns.pop(skill_id, None)


def _find_skill(skills, skill_id):
    for skill in skills:
        if skill.get("id") == skill_id:
            return skill
    return None


def _short_skill_name(name: str, max_len: int = 12) -> str:
    normalized = str(name).replace(" - ", " ").strip()
    if len(normalized) <= max_len:
        return normalized
    return normalized[:max_len].rstrip()


def _skill_tracker_status(state, skill, cooldowns, uses):
    skill_id = skill.get("id")
    label = _short_skill_name(skill.get("name", skill_id or "Skill"))

    if state.player.name == "Nasir" and skill_id == "adaptive_activate" and state.player.unique_vars.get("adaptive_locked", False):
        status = "LOCK"
    else:
        limit = skill.get("uses")
        used = int(uses.get(skill_id, 0))
        if limit is not None and used >= int(limit):
            status = "USED"
        else:
            cd = int(cooldowns.get(skill_id, 0))
            status = f"CD{cd}" if cd > 0 else "RDY"

    return f"{label}:{status}"


def _append_turn_skill_cooldown_log(state):
    ctx = state.context_flags
    cooldowns = ctx.get("player_cooldowns", {})
    uses = ctx.get("player_skill_uses", {})

    skill_states = [_skill_tracker_status(state, skill, cooldowns, uses) for skill in state.player.actives]
    cooldown_summary = ", ".join(skill_states) if skill_states else "No skills"

    effect_turns = ctx.get("effect_turns", {})
    active_effects = [
        (key, int(turns))
        for key, turns in effect_turns.items()
        if int(turns) > 0
    ]
    active_effects.sort(key=lambda pair: (-pair[1], pair[0]))

    if active_effects:
        effect_preview = [f"{name}:{turns}t" for name, turns in active_effects[:3]]
        if len(active_effects) > 3:
            effect_preview.append(f"+{len(active_effects) - 3}")
        effect_summary = ", ".join(effect_preview)
    else:
        effect_summary = "none"

    action_label = ctx.get("turn_action_label") or "No skill"
    tracker = ctx.setdefault("turn_skill_cooldown_log", [])
    tracker.append(
        {
            "turn": state.turn + 1,
            "action": action_label,
            "cooldowns": cooldown_summary,
            "effects": effect_summary,
        }
    )
    if len(tracker) > 24:
        tracker.pop(0)

    ctx["turn_action_label"] = None


def _reset_turn_flags(state):
    state.context_flags["turn_action_label"] = None
    state.context_flags["turn_flags"] = {
        "used_skill": False,
        "used_np": False,
        "rested": False,
        "attempted_dodge": False,
        "dodge_success": False,
        "blocked": False,
    }


def _prepare_block(state):
    if state.player.sp < SP_COST_BLOCK:
        state.log_event("Not enough SP to hold a defensive stance.")
        return False

    state.context_flags["player_blocking"] = True
    state.context_flags["turn_action_label"] = "BLOCK"
    state.context_flags["turn_flags"]["rested"] = False
    state.log_event("You brace for impact -- defensive stance locked.")
    return True
