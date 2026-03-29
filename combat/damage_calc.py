import random

from combat.combat_constants import BASE_DAMAGE_VARIANCE, CRIT_CHANCE_BASE, CRIT_MULTIPLIER


def _roll_variance(base_value: float, variance: float = BASE_DAMAGE_VARIANCE) -> float:
    low = 1.0 - variance
    high = 1.0 + variance
    return base_value * random.uniform(low, high)


def roll_crit(crit_chance: float = CRIT_CHANCE_BASE) -> bool:
    return random.random() < crit_chance


def calculate_damage(
    attack: int,
    defense_factor: float = 1.0,
    damage_multiplier: float = 1.0,
    variance: float = BASE_DAMAGE_VARIANCE,
    crit_chance: float = CRIT_CHANCE_BASE,
    crit_multiplier: float = CRIT_MULTIPLIER,
) -> tuple[int, bool]:
    base = max(0, attack) * max(0.0, damage_multiplier)
    rolled = _roll_variance(base, variance)
    is_crit = roll_crit(crit_chance)
    if is_crit:
        rolled *= crit_multiplier
    reduced = rolled * max(0.0, defense_factor)
    return max(1, int(round(reduced))), is_crit
