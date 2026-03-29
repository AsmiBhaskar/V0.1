from combat.passive_triggers import (
    HOOK_ON_DEATH,
    HOOK_ON_DODGE_SUC,
    HOOK_ON_TURN_START,
    register_hook,
)
from combat.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_nasir(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Nasir",
        servant_class="Lancer",
        is_enemy=is_enemy,
        strength=100,
        endurance=120,
        agility=100,
        mana_rank=200,
        luck=80,
        base_dodge=0.65,
        unique_vars={
            "consecutive_hits": 0,
            "battle_continuation_used": False,
            "zero_state_active": False,
            "adaptive_bonus": 0.0,
            "emotional_severance_turns": 0,
            "minds_eye_free_dodge_used": False,
        },
        passives={
            "perfected_form": True,
            "minds_eye": True,
            "adaptive_evolution": True,
            "hardened_discipline": True,
            "emotional_severance": True,
            "cursed_physique": True,
        },
        actives=[
            {
                "id": "zuxi_combat_call",
                "name": "Zuxi - Combat Call",
                "mana_cost": 20,
                "cooldown": 0,
                "damage_mult": 1.5,
                "effect": "mana_burst",
            },
            {
                "id": "adaptive_activate",
                "name": "Adaptive Evolution",
                "mana_cost": 15,
                "cooldown": 3,
                "effect": "guaranteed_dodge",
            },
            {
                "id": "emotional_sev_act",
                "name": "Emotional Severance",
                "mana_cost": 10,
                "cooldown": 5,
                "effect": "clear_fear",
            },
            {
                "id": "hardened_disc_act",
                "name": "Hardened Discipline",
                "mana_cost": 30,
                "cooldown": None,
                "uses": 1,
                "effect": "zero_state",
            },
        ],
        np_item={
            "id": "zuxi_sealed",
            "name": "Zuxi (Sealed)",
            "base_mana_cost": 50,
            "true_name_cost": 60,
            "true_name_effect": "guaranteed_hit_all_defense_bypass",
            "once_per_battle": True,
        },
    )
    _register_nasir_hooks()
    return servant


def _register_nasir_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        if state.turn > 0 and state.turn % 2 == 0:
            uv["adaptive_bonus"] = min(uv["adaptive_bonus"] + 0.03, 0.15)
            state.player.base_dodge = 0.65 + uv["adaptive_bonus"]

        if uv.get("emotional_severance_turns", 0) > 0:
            uv["emotional_severance_turns"] -= 1

    def on_dodge_success(state, ctx):
        uv = state.player.unique_vars
        uv["consecutive_hits"] = uv.get("consecutive_hits", 0) + 1

    def on_death(state, ctx):
        uv = state.player.unique_vars
        if not uv.get("battle_continuation_used", False):
            state.player.hp = 1
            state.player.sp = 1
            uv["battle_continuation_used"] = True
            state.log_event("Hardened Discipline - Nasir endures.")

    register_hook(HOOK_ON_TURN_START, "Nasir", on_turn_start)
    register_hook(HOOK_ON_DODGE_SUC, "Nasir", on_dodge_success)
    register_hook(HOOK_ON_DEATH, "Nasir", on_death)
    _HOOKS_REGISTERED = True
