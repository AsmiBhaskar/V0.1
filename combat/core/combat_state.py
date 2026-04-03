from dataclasses import dataclass, field

from combat.entities.servant_base import ServantBase


@dataclass
class CombatState:
    player: ServantBase
    enemy: ServantBase
    turn: int = 0
    phase: str = "player_action"
    log: list[str] = field(default_factory=list)

    consecutive_dodges: int = 0
    dodge_ready: bool = False

    player_statuses: list = field(default_factory=list)
    enemy_statuses: list = field(default_factory=list)

    context_flags: dict = field(default_factory=dict)

    def log_event(self, text: str):
        self.log.append(text)
        if len(self.log) > 50:
            self.log.pop(0)

