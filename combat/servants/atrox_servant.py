from combat.systems.passive_triggers import HOOK_ON_DODGE_SUC, HOOK_ON_LOW_SP, HOOK_ON_TURN_START, register_hook
from combat.entities.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_atrox(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Atrox",
        servant_class="Rider",
        is_enemy=is_enemy,
        strength=110,
        endurance=110,
        agility=80,
        mana_rank=300,
        luck=60,
        base_dodge=0.50,
        unique_vars={
            "defense_debuff_stacks": 0,
            "iron_path_active": False,
        },
        passives={
            "cutting_corners": True,
            "beyond_all_reason": True,
            "favoured_by_evil": True,
            "homeward": True,
        },
        actives=[
            {
                "id": "cutting_corners_act",
                "name": "Cutting Corners",
                "mana_cost": 15,
                "cooldown": 3,
                "effect": "target_defense_down",
            },
            {
                "id": "beyond_all_reason_act",
                "name": "Beyond All Reason",
                "mana_cost": 20,
                "cooldown": 4,
                "effect": "damage_down_dodge_up",
            },
            {
                "id": "favoured_by_evil_summon",
                "name": "Favoured by Evil",
                "mana_cost": 35,
                "cooldown": None,
                "uses": 1,
                "effect": "summon_spirit",
            },
            {
                "id": "iron_path_phase_1",
                "name": "Iron Path (Phase I)",
                "mana_cost": 25,
                "cooldown": 3,
                "effect": "iron_path_mode",
            },
        ],
        np_item={
            "id": "iron_path_relic",
            "name": "Iron Path Relic",
            "base_mana_cost": 60,
            "true_name_cost": 60,
            "true_name_effect": "iron_path_three_phase_massive_damage",
            "once_per_battle": True,
        },
    )
    _register_atrox_hooks()
    return servant


def _register_atrox_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        uv["defense_debuff_stacks"] = min(5, uv.get("defense_debuff_stacks", 0) + 1)

    def on_dodge_success(state, ctx):
        state.player.sp = min(state.player.sp_max, state.player.sp + 5)

    def on_low_sp(state, ctx):
        if state.player.sp < int(state.player.sp_max * 0.30):
            state.player.sp = min(state.player.sp_max, state.player.sp + 10)

    register_hook(HOOK_ON_TURN_START, "Atrox", on_turn_start)
    register_hook(HOOK_ON_DODGE_SUC, "Atrox", on_dodge_success)
    register_hook(HOOK_ON_LOW_SP, "Atrox", on_low_sp)
    _HOOKS_REGISTERED = True

