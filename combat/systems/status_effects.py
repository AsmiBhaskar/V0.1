from dataclasses import dataclass
from typing import Any, Callable


StatusCallback = Callable[[Any, Any, "StatusEffect"], None]


@dataclass
class StatusEffect:
    id: str
    name: str
    duration: int
    potency: float = 0.0
    on_apply: StatusCallback | None = None
    on_tick: StatusCallback | None = None
    on_expire: StatusCallback | None = None


def apply_status(statuses: list[StatusEffect], owner: Any, state: Any, status: StatusEffect):
    statuses.append(status)
    if status.on_apply:
        status.on_apply(owner, state, status)


def tick_statuses(statuses: list[StatusEffect], owner: Any, state: Any):
    expired: list[StatusEffect] = []
    for status in list(statuses):
        if status.on_tick:
            status.on_tick(owner, state, status)
        status.duration -= 1
        if status.duration <= 0:
            expired.append(status)

    for status in expired:
        if status.on_expire:
            status.on_expire(owner, state, status)
        statuses.remove(status)
