from combat.passive_triggers import HOOK_ON_SKILL_USE, HOOK_ON_TURN_START, register_hook
from combat.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_kiki(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Kiki",
        servant_class="Caster",
        is_enemy=is_enemy,
        strength=40,
        endurance=90,
        agility=60,
        mana_rank=500,
        luck=80,
        base_dodge=0.60,
        unique_vars={
            "territory_active": False,
            "territory_turns": 0,
        },
        passives={
            "gaze_of_admin": True,
            "muted_matrix": True,
            "segmentation_passive": True,
        },
        actives=[
            {
                "id": "segmentation",
                "name": "Segmentation",
                "mana_cost": 25,
                "cooldown": 4,
                "effect": "enemy_damage_down",
            },
            {
                "id": "gaze_admin_act",
                "name": "Gaze of Admin",
                "mana_cost": 15,
                "cooldown": 2,
                "effect": "reveal_and_dodge_boost",
            },
            {
                "id": "territory_creation",
                "name": "Territory Creation",
                "mana_cost": 40,
                "cooldown": None,
                "uses": 1,
                "effect": "territory_field",
            },
            {
                "id": "correction_protocol",
                "name": "Correction Protocol",
                "mana_cost": 20,
                "cooldown": 3,
                "effect": "cleanse_and_sp_restore",
            },
        ],
        np_item={
            "id": "core_matrix_token",
            "name": "Core Matrix Token",
            "base_mana_cost": 50,
            "true_name_cost": 50,
            "true_name_effect": "predictable_patterns_team_boost",
            "once_per_battle": True,
        },
    )
    _register_kiki_hooks()
    return servant


def _register_kiki_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_skill_use(state, ctx):
        state.context_flags["kiki_cast_time_ignored"] = True

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        if uv.get("territory_active", False):
            uv["territory_turns"] = max(0, uv.get("territory_turns", 0) - 1)
            state.player.base_dodge = 0.70
            if uv["territory_turns"] == 0:
                uv["territory_active"] = False
                state.player.base_dodge = 0.60
                state.log_event("Territory Creation fades from the battlefield.")

    register_hook(HOOK_ON_SKILL_USE, "Kiki", on_skill_use)
    register_hook(HOOK_ON_TURN_START, "Kiki", on_turn_start)
    _HOOKS_REGISTERED = True
