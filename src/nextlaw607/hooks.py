from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class HookEvent(str, Enum):
    PRE_MODEL = "pre-model"
    PRE_TOOL = "pre-tool"
    POST_TOOL = "post-tool"
    STOP = "stop"


@dataclass(frozen=True)
class HookResult:
    allowed: bool
    reason: str = ""


Hook = Callable[[dict[str, object]], HookResult]


class HookEnforcementBus:
    def __init__(self) -> None:
        self._hooks: dict[HookEvent, list[Hook]] = {event: [] for event in HookEvent}

    def register(self, event: HookEvent, hook: Hook) -> None:
        self._hooks[event].append(hook)

    def enforce(self, event: HookEvent, context: dict[str, object]) -> None:
        for hook in self._hooks[event]:
            result = hook(dict(context))
            if not isinstance(result, HookResult):
                raise TypeError("hook must return HookResult")
            if not result.allowed:
                raise PermissionError(result.reason or f"{event.value} hook denied")
