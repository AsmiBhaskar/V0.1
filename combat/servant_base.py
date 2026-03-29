from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServantBase:
    name: str
    servant_class: str
    is_enemy: bool = False

    strength: int = 60
    endurance: int = 60
    agility: int = 60
    mana_rank: int = 60
    luck: int = 60

    hp_max: int = 0
    hp: int = 0
    sp_max: int = 0
    sp: int = 0
    mana_max: int = 0
    mana: int = 0

    base_dodge: float = 0.50
    base_attack: int = 0

    passives: dict[str, Any] = field(default_factory=dict)
    actives: list[dict[str, Any]] = field(default_factory=list)
    np_item: dict[str, Any] = field(default_factory=dict)

    unique_vars: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        from combat.combat_constants import END_TO_SP, MANA_TO_BASE

        self.hp_max = self.strength * 12
        self.hp = self.hp_max
        self.sp_max = END_TO_SP.get(str(self.endurance), self.endurance)
        self.sp = self.sp_max
        self.mana_max = MANA_TO_BASE.get(str(self.mana_rank), self.mana_rank)
        self.mana = self.mana_max
        self.base_attack = self.strength
