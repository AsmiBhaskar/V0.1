from combat.systems.passive_triggers import HOOK_ON_LOW_HP, HOOK_ON_TURN_START, register_hook
from combat.entities.servant_base import ServantBase

_HOOKS_REGISTERED = False


def make_kitik(is_enemy: bool = False) -> ServantBase:
    servant = ServantBase(
        name="Kitik",
        servant_class="Archer",
        is_enemy=is_enemy,
        strength=60,
        endurance=100,
        agility=95,
        mana_rank=300,
        luck=110,
        base_dodge=0.50,
        unique_vars={
            "song_bonus": 0.0,
            "song_triggered": False,
        },
        passives={
            "song_of_sorrow": True,
            "dominance_of_decision": True,
            "absolute_aim_passive": True,
        },
        actives=[
            {
                "id": "mystic_eyes_sniper",
                "name": "Mystic Eyes - Sniper",
                "mana_cost": 35,
                "cooldown": 4,
                "effect": "mystic_eyes_sniper",
            },
            {
                "id": "mana_burst",
                "name": "Mana Burst",
                "mana_cost": 20,
                "cooldown": 0,
                "effect": "mana_burst",
                "damage_mult": 1.7,
            },
            {
                "id": "improvised_arrow",
                "name": "Improvised Arrow",
                "mana_cost": 10,
                "cooldown": 0,
                "effect": "improvised_arrow",
                "damage_mult": 1.3,
            },
            {
                "id": "song_of_sorrow_act",
                "name": "Song of Sorrow",
                "mana_cost": 30,
                "cooldown": None,
                "uses": 1,
                "effect": "emergency_heal",
            },
        ],
        np_item={
            "id": "grand_verdict_score",
            "name": "Grand Verdict - Opera of the Unignorable Court",
            "base_mana_cost": 55,
            "true_name_cost": 55,
            "base_effect": "grand_verdict_reality_marble",
            "true_name_effect": "grand_verdict_reality_marble_true_name",
            "once_per_battle": True,
        },
    )
    _register_kitik_hooks()
    return servant


def _register_kitik_hooks():
    global _HOOKS_REGISTERED
    if _HOOKS_REGISTERED:
        return

    def on_turn_start(state, ctx):
        uv = state.player.unique_vars
        uv["song_bonus"] = uv.get("song_bonus", 0.0) + 0.05

    def on_low_hp(state, ctx):
        uv = state.player.unique_vars
        if uv.get("song_triggered", False):
            ctx["consumed"] = True
            return
        threshold = int(state.player.hp_max * 0.20)
        if state.player.hp <= threshold:
            state.player.hp = min(state.player.hp_max, state.player.hp + int(state.player.hp_max * 0.20))
            uv["song_triggered"] = True
            ctx["consumed"] = True
            state.log_event("Song of Sorrow - Kitik stabilizes with a final refrain.")
        else:
            ctx["consumed"] = False

    register_hook(HOOK_ON_TURN_START, "Kitik", on_turn_start)
    register_hook(HOOK_ON_LOW_HP, "Kitik", on_low_hp)
    _HOOKS_REGISTERED = True

