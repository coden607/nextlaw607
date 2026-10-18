from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .execution_state import RunScope


@dataclass(frozen=True)
class MemoryScope:
    user_id: str
    matter_id: str

    @classmethod
    def from_run_scope(cls, scope: RunScope) -> "MemoryScope":
        return cls(user_id=scope.user_id, matter_id=scope.matter_id)

    def matches(self, other: "MemoryScope") -> bool:
        return self.user_id == other.user_id and self.matter_id == other.matter_id


class MatterMemoryStore:
    """In-memory exact-scope second-brain adapter.

    Workflow memory is non-authoritative and may never promote legal authority.
    """

    def __init__(self) -> None:
        self._items: dict[MemoryScope, dict[str, Any]] = {}

    def put(self, scope: MemoryScope, key: str, value: Any) -> None:
        key = key.strip()
        if not key:
            raise ValueError("key is required")
        self._items.setdefault(scope, {})[key] = value

    def get(self, scope: MemoryScope, key: str) -> Any | None:
        return self._items.get(scope, {}).get(key)

    def snapshot(self, scope: MemoryScope) -> dict[str, Any]:
        return dict(self._items.get(scope, {}))

    @staticmethod
    def authority_eligible() -> bool:
        return False
