from combat.data.combat_constants import (
    EXHAUSTION_THRESHOLD,
    EXHAUSTION_PENALTY,
    FATIGUE_SP_PENALTY,
    FATIGUE_THRESHOLD,
    SP_COST_MINIMUM,
    SP_COST_PER_DODGE,
)


def calculate_dodge_modifier(agi: int, lck: int) -> float:
    return min((agi * 0.3) + (lck * 0.2), 100.0)


def calculate_dodge_chance(
    base_dodge: float,
    sp_current: int,
    sp_max: int,
    agi: int,
    lck: int,
) -> float:
    if sp_max <= 0:
        return 0.0
    sp_ratio = sp_current / sp_max
    modifier = calculate_dodge_modifier(agi, lck)
    exhaustion = EXHAUSTION_PENALTY if sp_current < EXHAUSTION_THRESHOLD else 1.0
    return (base_dodge * sp_ratio * modifier * exhaustion) / 100


def calculate_sp_cost(consecutive_dodges: int, perfected_form: bool = False) -> int:
    cost = SP_COST_PER_DODGE - (5 if perfected_form else 0)
    if consecutive_dodges >= FATIGUE_THRESHOLD:
        cost += FATIGUE_SP_PENALTY * (consecutive_dodges - (FATIGUE_THRESHOLD - 1))
    return max(cost, SP_COST_MINIMUM)


def attempt_dodge(servant, consecutive_dodges: int, perfected_form: bool = False) -> tuple[bool, int]:
    import random

    chance = calculate_dodge_chance(
        servant.base_dodge,
        servant.sp,
        servant.sp_max,
        servant.agility,
        servant.luck,
    )
    success = random.random() < chance
    sp_cost = calculate_sp_cost(consecutive_dodges, perfected_form) if success else 0
    return success, sp_cost

