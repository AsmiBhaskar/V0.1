from combat.systems.passive_triggers import HOOK_ON_HIT, HOOK_ON_TURN_START, register_hook
from combat.entities.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_stella(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Stella",
        servant_class="Assassin",
        is_enemy=is_enemy,
        strength=40,
        endurance=90,
        agility=100,
        mana_rank=400,
        luck=100,
        base_dodge=0.50,
        unique_vars={
            "profile_complete": False,
            "profile_turns": 0,
            "first_attack_auto_dodge_used": False,
        },
        passives={
            "data_lake": True,
            "cautious_step": True,
            "whisper_network": True,
            "outcast_affinity": True,
        },
        actives=[
            {
                "id": "whisper_network_act",
                "name": "Whisper Network",
                "mana_cost": 15,
                "cooldown": 0,
                "effect": "next_attack_amp",
                "damage_mult": 1.5,
            },
            {
                "id": "academic_perfection",
                "name": "Academic Perfection",
                "mana_cost": 10,
                "cooldown": 2,
                "effect": "guaranteed_crit_next",
            },
            {
                "id": "data_lake_act",
                "name": "Data Lake",
                "mana_cost": 20,
                "cooldown": 3,
                "effect": "instant_profile",
            },
            {
                "id": "stellae_scriptum",
                "name": "Stellae Scriptum",
                "mana_cost": 50,
                "cooldown": None,
                "uses": 1,
                "effect": "permanent_enemy_stat_down",
            },
        ],
        np_item={
            "id": "codex_page",
            "name": "Codex Page",
            "base_mana_cost": 50,
            "true_name_cost": 50,
            "true_name_effect": "rewrite_legend_stat_down",
            "once_per_battle": True,
        },
    )
    _register_stella_hooks()
    return servant


def _register_stella_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        uv["profile_turns"] = uv.get("profile_turns", 0) + 1
        if not uv.get("profile_complete", False) and uv["profile_turns"] >= 2:
            uv["profile_complete"] = True
            state.player.base_dodge = 0.65
            state.log_event("Data Lake complete - Stella maps every opening.")

    def on_hit(state, ctx):
        state.context_flags["enemy_next_attack_revealed"] = True

    register_hook(HOOK_ON_TURN_START, "Stella", on_turn_start)
    register_hook(HOOK_ON_HIT, "Stella", on_hit)
    _HOOKS_REGISTERED = True

