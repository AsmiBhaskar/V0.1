from combat.systems.passive_triggers import HOOK_ON_DEATH, HOOK_ON_HIT_RECV, HOOK_ON_TURN_START, register_hook
from combat.entities.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_bhaskar(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Bhaskar",
        servant_class="Berserker",
        is_enemy=is_enemy,
        strength=110,
        endurance=110,
        agility=80,
        mana_rank=200,
        luck=40,
        base_dodge=0.50,
        unique_vars={
            "rage_meter": 0,
            "recursion_count": 0,
            "ache_level": 0,
            "rage_damage_bonus": 0.0,
            "cardinal_bonus": 0.0,
        },
        passives={
            "recursion": True,
            "oblivious_exception": True,
            "cardinal_algorithm": True,
            "rage_against_unjust": True,
            "sickness_of_unholy_blood": True,
        },
        actives=[
            {
                "id": "rage_unjust_act",
                "name": "Rage Against Unjust",
                "mana_cost": 0,
                "cooldown": 3,
                "effect": "rage_mode",
            },
            {
                "id": "cardinal_algorithm_act",
                "name": "Cardinal Algorithm",
                "mana_cost": 15,
                "cooldown": 4,
                "effect": "pattern_analysis",
            },
            {
                "id": "cheat_gainer",
                "name": "Cheat Gainer",
                "mana_cost": 20,
                "cooldown": None,
                "uses": 1,
                "effect": "copy_enemy_skill",
            },
            {
                "id": "divine_spear_skill",
                "name": "Divine Spear - Bhaskar",
                "mana_cost": 30,
                "cooldown": 2,
                "effect": "heavy_hit_stun_self",
                "damage_mult": 2.5,
            },
        ],
        np_item={
            "id": "divine_spear_fragment",
            "name": "Divine Spear Fragment",
            "base_mana_cost": 70,
            "true_name_cost": 70,
            "true_name_effect": "devastation_exposed_after",
            "once_per_battle": True,
        },
    )
    _register_bhaskar_hooks()
    return servant


def _register_bhaskar_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        if state.turn > 0 and state.turn % 2 == 0:
            uv["cardinal_bonus"] = min(uv.get("cardinal_bonus", 0.0) + 0.05, 0.25)

        dodge = 0.50 + uv.get("cardinal_bonus", 0.0)
        if state.player.hp <= int(state.player.hp_max * 0.30):
            dodge -= 0.15
        state.player.base_dodge = max(0.10, dodge)

    def on_hit_received(state, ctx):
        uv = state.player.unique_vars
        uv["rage_meter"] = min(100, uv.get("rage_meter", 0) + 10)

        if state.player.hp <= int(state.player.hp_max * 0.50):
            uv["rage_damage_bonus"] = min(0.50, uv.get("rage_damage_bonus", 0.0) + 0.10)

    def on_death(state, ctx):
        uv = state.player.unique_vars
        recursion_count = uv.get("recursion_count", 0)
        if recursion_count < 3:
            uv["recursion_count"] = recursion_count + 1
            state.player.hp_max = max(1, int(state.player.hp_max * 0.85))
            state.player.hp = max(1, int(state.player.hp_max * 0.30))
            state.log_event("Recursion - Bhaskar rises again through impossible force.")

    register_hook(HOOK_ON_TURN_START, "Bhaskar", on_turn_start)
    register_hook(HOOK_ON_HIT_RECV, "Bhaskar", on_hit_received)
    register_hook(HOOK_ON_DEATH, "Bhaskar", on_death)
    _HOOKS_REGISTERED = True

