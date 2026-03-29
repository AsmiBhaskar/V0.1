import random

from combat.servant_base import ServantBase

SPIRIT_POOL = [
    {"name": "Wandering Shade", "strength": 40, "agility": 40, "luck": 20},
    {"name": "Iron Remnant", "strength": 60, "agility": 30, "luck": 30},
    {"name": "Bound Horseman", "strength": 50, "agility": 60, "luck": 40},
]


def make_random_spirit() -> ServantBase:
    data = random.choice(SPIRIT_POOL)
    return ServantBase(
        name=data["name"],
        servant_class="Spirit",
        is_enemy=True,
        strength=data["strength"],
        agility=data["agility"],
        luck=data["luck"],
        endurance=40,
        mana_rank=50,
        passives={},
        actives=[],
        np_item={},
    )
