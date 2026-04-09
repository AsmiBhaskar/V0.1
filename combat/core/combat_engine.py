import logging

import pygame

from combat.data.combat_constants import (
    ACTIONS,
    ACTION_ACT,
    ACTION_BLOCK,
    ACTION_DODGE,
    ACTION_FIGHT,
    ACTION_ITEM,
    ACTION_NP,
    MAX_TURNS,
)
from combat.core.combat_result import CombatResult
from combat.core.combat_state import CombatState
from combat.ui.combat_renderer import render_combat_frame
from combat.data.item_data import ITEMS
from combat.systems.passive_triggers import HOOK_ON_TURN_END, HOOK_ON_TURN_START, fire_hook
from combat.core.turn_manager import get_skill_mana_cost, initialize_runtime_state, process_enemy_turn, process_player_action
from game_core.constants import FPS

LOGGER = logging.getLogger(__name__)


def run_combat(screen, clock, encounter: dict) -> CombatResult:
    context = dict(encounter.get("context", {}))

    player = encounter["player_fn"]()
    enemy = _build_enemy(encounter, context)

    state = CombatState(
        player=player,
        enemy=enemy,
        context_flags=context,
    )
    initialize_runtime_state(state)

    title = encounter.get("title", "ENCOUNTER")
    state.log_event(f"{title}")
    state.log_event(f"{player.name} vs {enemy.name}")
    LOGGER.info(
        "Combat start | title=%s | player=%s | enemy=%s | context=%s",
        title,
        player.name,
        enemy.name,
        context,
    )

    _apply_context_modifiers(state)
    _reset_ui_state(state)

    selected_action = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LOGGER.info("Combat interrupted by quit | %s", _combat_snapshot(state))
                return CombatResult(
                    winner="draw",
                    hp_remaining=state.player.hp,
                    sp_remaining=state.player.sp,
                    mana_remaining=state.player.mana,
                    turns_taken=state.turn,
                )

            if event.type == pygame.KEYDOWN:
                payload = _handle_keydown(event.key, state)
                if payload is not None:
                    selected_action = payload

        if state.phase == "player_action" and selected_action:
            LOGGER.info("Turn %d | player_action payload=%s", state.turn + 1, selected_action)
            if not state.context_flags.get("turn_start_hook_fired", False):
                fire_hook(HOOK_ON_TURN_START, state, state.player.name, {"turn": state.turn})
                state.context_flags["turn_start_hook_fired"] = True
            result = process_player_action(state, selected_action)
            selected_action = None
            if result:
                finalized = _finalize_result_for_context(state, result)
                LOGGER.info(
                    "Combat end | phase=player_action | winner=%s | turns=%d | flags=%s | %s",
                    finalized.winner,
                    finalized.turns_taken,
                    finalized.flags,
                    _combat_snapshot(state),
                )
                return finalized

        elif state.phase == "enemy_attack":
            result = process_enemy_turn(state)
            if result:
                finalized = _finalize_result_for_context(state, result)
                LOGGER.info(
                    "Combat end | phase=enemy_attack | winner=%s | turns=%d | flags=%s | %s",
                    finalized.winner,
                    finalized.turns_taken,
                    finalized.flags,
                    _combat_snapshot(state),
                )
                return finalized

        elif state.phase == "dodge_phase":
            if "dodge_choice" in state.context_flags:
                result = process_enemy_turn(state)
                if result:
                    finalized = _finalize_result_for_context(state, result)
                    LOGGER.info(
                        "Combat end | phase=dodge_phase | winner=%s | turns=%d | flags=%s | %s",
                        finalized.winner,
                        finalized.turns_taken,
                        finalized.flags,
                        _combat_snapshot(state),
                    )
                    return finalized

                if state.phase == "player_action":
                    fire_hook(HOOK_ON_TURN_END, state, state.player.name, {"turn": state.turn})
                    state.turn += 1
                    state.context_flags["turn_start_hook_fired"] = False
                    LOGGER.info("Turn %d complete | %s", state.turn, _combat_snapshot(state))

                    if state.turn >= MAX_TURNS:
                        LOGGER.info("Combat ended by turn limit | %s", _combat_snapshot(state))
                        return CombatResult(
                            winner="draw",
                            hp_remaining=state.player.hp,
                            sp_remaining=state.player.sp,
                            mana_remaining=state.player.mana,
                            turns_taken=state.turn,
                            flags=["turn_limit_reached"],
                        )

        render_combat_frame(screen, state, title)
        pygame.display.flip()
        clock.tick(FPS)


def _build_enemy(encounter: dict, context: dict):
    enemy_fn = encounter.get("enemy_fn")
    if callable(enemy_fn):
        return enemy_fn()

    if context.get("spirit_hunt"):
        from combat.data.spirit_data import make_random_spirit

        return make_random_spirit()

    if context.get("ache_active"):
        from combat.data.ache_enemy_data import make_random_ache_enemy

        return make_random_ache_enemy()

    from combat.data.spirit_data import make_random_spirit

    return make_random_spirit()


def _apply_context_modifiers(state):
    context = state.context_flags

    if context.get("assassin_scripted_loss"):
        state.context_flags["core_matrix_active"] = True
        state.context_flags["reality_field_owner"] = "enemy"
        state.player.base_dodge = max(0.05, state.player.base_dodge - 0.20)
        state.enemy.base_dodge = min(0.90, state.enemy.base_dodge + 0.15)
        state.enemy.base_attack = int(round(state.enemy.base_attack * 1.25))
        state.log_event("Core Matrix saturates the field. Stella's movement reads as predictable.")
        state.log_event("Kiki's pressure spikes - this battle is overwhelmingly one-sided.")

    if context.get("assassin_berserker_cutscene"):
        state.player.base_dodge = max(0.05, state.player.base_dodge - 0.10)
        state.enemy.base_attack = int(round(state.enemy.base_attack * 1.15))
        state.context_flags["enemy_np"] = max(int(state.context_flags.get("enemy_np", 0)), 60)
        state.log_event("The Burning Sun descends - pressure and heat distort every escape line.")

    if context.get("assassin_scene9_final_hook"):
        state.player.base_dodge = max(0.05, state.player.base_dodge - 0.05)
        state.context_flags["enemy_np"] = max(int(state.context_flags.get("enemy_np", 0)), 30)
        state.log_event("An unknown signal manifests as hostile pressure in the hunt corridor.")

    if context.get("ache_active"):
        ache = int(state.player.unique_vars.get("ache_level", 0))
        state.context_flags["ache_start"] = ache
        state.player.base_dodge = max(0.05, state.player.base_dodge - (ache * 0.02))
        state.player.unique_vars["rage_meter"] = state.player.unique_vars.get("rage_meter", 0) + (ache * 5)
        state.log_event(f"Burning Ache: Level {ache} - clarity fractures.")

    if context.get("spirit_hunt"):
        state.log_event("Spirit Hunt conditions active.")


def _reset_ui_state(state):
    state.context_flags["action_index"] = 0
    state.context_flags["submenu_open"] = False
    state.context_flags["submenu_title"] = ""
    state.context_flags["submenu_options"] = []
    state.context_flags["submenu_index"] = 0


def _handle_keydown(key, state):
    if state.phase == "dodge_phase":
        if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
            state.context_flags["dodge_choice"] = True
        elif key == pygame.K_ESCAPE:
            state.context_flags["dodge_choice"] = False
        return None

    if state.phase != "player_action":
        return None

    if state.context_flags.get("submenu_open", False):
        return _handle_submenu_key(key, state)

    if key in (pygame.K_LEFT, pygame.K_UP):
        state.context_flags["action_index"] = (state.context_flags["action_index"] - 1) % len(ACTIONS)
        return None

    if key in (pygame.K_RIGHT, pygame.K_DOWN):
        state.context_flags["action_index"] = (state.context_flags["action_index"] + 1) % len(ACTIONS)
        return None

    direct = {
        pygame.K_f: ACTION_FIGHT,
        pygame.K_a: ACTION_ACT,
        pygame.K_i: ACTION_ITEM,
        pygame.K_n: ACTION_NP,
        pygame.K_d: ACTION_DODGE,
        pygame.K_b: ACTION_BLOCK,
    }

    if key in direct:
        action = direct[key]
        if action in ACTIONS:
            state.context_flags["action_index"] = ACTIONS.index(action)
        return _activate_or_open_submenu(action, state)

    if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        action = ACTIONS[state.context_flags.get("action_index", 0)]
        return _activate_or_open_submenu(action, state)

    return None


def _handle_submenu_key(key, state):
    options = state.context_flags.get("submenu_options", [])
    if not options:
        _close_submenu(state)
        return None

    if key in (pygame.K_UP, pygame.K_LEFT):
        state.context_flags["submenu_index"] = (state.context_flags["submenu_index"] - 1) % len(options)
        return None

    if key in (pygame.K_DOWN, pygame.K_RIGHT):
        state.context_flags["submenu_index"] = (state.context_flags["submenu_index"] + 1) % len(options)
        return None

    if key == pygame.K_ESCAPE:
        _close_submenu(state)
        return None

    if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        idx = state.context_flags.get("submenu_index", 0)
        payload = options[idx]["payload"]
        _close_submenu(state)
        return payload

    return None


def _activate_or_open_submenu(action: str, state):
    if action == ACTION_ACT:
        options = []
        uses = state.context_flags.get("player_skill_uses", {})
        for skill in state.player.actives:
            mana_cost = get_skill_mana_cost(skill, uses)
            label = f"{skill['name']}  |  Mana {mana_cost}"
            options.append(
                {
                    "label": label,
                    "payload": {"action": ACTION_ACT, "skill_id": skill.get("id")},
                }
            )

        if not options:
            state.log_event("No active skills available.")
            return None

        _open_submenu(state, "ACT SKILLS", options)
        return None

    if action == ACTION_ITEM:
        inventory = list(state.context_flags.get("inventory", []))
        options = []
        for item_id in inventory:
            item = ITEMS.get(item_id)
            if not item:
                continue
            label = f"{item['name']}  |  +{item.get('restore', 0)} {item.get('category', '').upper()}"
            options.append(
                {
                    "label": label,
                    "payload": {"action": ACTION_ITEM, "item_id": item_id},
                }
            )

        if not options:
            state.log_event("Inventory is empty.")
            return None

        _open_submenu(state, "ITEMS", options)
        return None

    if action == ACTION_NP:
        np_item = state.player.np_item
        if not np_item:
            state.log_event("No Noble Phantasm equipped.")
            return None

        options = [
            {
                "label": f"{np_item['name']}  |  Mana {np_item.get('base_mana_cost', 50)}",
                "payload": {"action": ACTION_NP, "mode": "base"},
            }
        ]

        true_cost = np_item.get("true_name_cost")
        if true_cost is not None:
            options.append(
                {
                    "label": f"True Name Release  |  Mana {true_cost}",
                    "payload": {"action": ACTION_NP, "mode": "true_name"},
                }
            )

        _open_submenu(state, "NOBLE PHANTASM", options)
        return None

    return {"action": action}


def _open_submenu(state, title: str, options: list[dict]):
    state.context_flags["submenu_open"] = True
    state.context_flags["submenu_title"] = title
    state.context_flags["submenu_options"] = options
    state.context_flags["submenu_index"] = 0


def _close_submenu(state):
    state.context_flags["submenu_open"] = False
    state.context_flags["submenu_title"] = ""
    state.context_flags["submenu_options"] = []
    state.context_flags["submenu_index"] = 0


def _finalize_result_for_context(state, result: CombatResult) -> CombatResult:
    if state.context_flags.get("ache_active") and result.winner == "player":
        ache_level = int(state.player.unique_vars.get("ache_level", 0))
        state.player.unique_vars["ache_level"] = max(0, ache_level - 1)

    if state.context_flags.get("spirit_hunt") and result.winner == "player" and "spirit_captured" not in result.flags:
        result.flags.append("spirit_captured")

    return result


def _combat_snapshot(state) -> str:
    return (
        f"P(HP={state.player.hp}/{state.player.hp_max},SP={state.player.sp}/{state.player.sp_max},"
        f"M={state.player.mana}/{state.player.mana_max}) "
        f"E(HP={state.enemy.hp}/{state.enemy.hp_max},SP={state.enemy.sp}/{state.enemy.sp_max},"
        f"M={state.enemy.mana}/{state.enemy.mana_max})"
    )

