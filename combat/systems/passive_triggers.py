from typing import Callable


HOOK_ON_HIT = "on_hit"
HOOK_ON_HIT_RECV = "on_hit_received"
HOOK_ON_DODGE_SUC = "on_dodge_success"
HOOK_ON_DODGE_FAIL = "on_dodge_fail"
HOOK_ON_TURN_START = "on_turn_start"
HOOK_ON_TURN_END = "on_turn_end"
HOOK_ON_LOW_HP = "on_low_hp"
HOOK_ON_LOW_SP = "on_low_sp"
HOOK_ON_DEATH = "on_death"
HOOK_ON_SKILL_USE = "on_skill_use"
HOOK_ON_NP_USE = "on_np_use"

_REGISTRY: dict[str, list[tuple[str, Callable]]] = {}


def register_hook(hook_name: str, servant_name: str, fn: Callable):
    handlers = _REGISTRY.setdefault(hook_name, [])
    for name, existing in handlers:
        if name == servant_name and getattr(existing, "__name__", None) == getattr(fn, "__name__", None):
            return
    handlers.append((servant_name, fn))


def fire_hook(hook_name: str, state, servant_name: str, ctx: dict | None = None):
    ctx = ctx or {}
    for name, fn in _REGISTRY.get(hook_name, []):
        if name == servant_name:
            fn(state, ctx)
