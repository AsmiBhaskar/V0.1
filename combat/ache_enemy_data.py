import random

from combat.servant_base import ServantBase

ACHE_POOL = [
    {"name": "Fractured Echo", "strength": 65, "agility": 55, "luck": 30},
    {"name": "Smoldering Husk", "strength": 75, "agility": 40, "luck": 25},
    {"name": "Sunless Reflection", "strength": 70, "agility": 60, "luck": 35},
]


def make_random_ache_enemy() -> ServantBase:
    data = random.choice(ACHE_POOL)
    return ServantBase(
        name=data["name"],
        servant_class="Ache",
        is_enemy=True,
        strength=data["strength"],
        agility=data["agility"],
        luck=data["luck"],
        endurance=60,
        mana_rank=80,
        passives={},
        actives=[],
        np_item={},
    )
