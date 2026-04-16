from combat.systems.passive_triggers import HOOK_ON_HIT, register_hook
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
            "data_lake_active": False,
            "data_lake_turns": 0,
            "data_lake_cooldown": 0,
            "update_profile_available": False,
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
                "cooldown": 0,
                "effect": "data_lake_activate",
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

    def on_hit(state, ctx):
        state.context_flags["enemy_next_attack_revealed"] = True

    register_hook(HOOK_ON_HIT, "Stella", on_hit)
    _HOOKS_REGISTERED = True

