from dataclasses import dataclass, field


@dataclass
class CombatResult:
    winner: str
    hp_remaining: int = 0
    sp_remaining: int = 0
    mana_remaining: int = 0
    turns_taken: int = 0
    flags: list[str] = field(default_factory=list)
