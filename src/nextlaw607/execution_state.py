from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _required(value: str, name: str) -> str:
    normalized = value.strip() if isinstance(value, str) else ""
    if not normalized or normalized == "*":
        raise ValueError(f"{name} is required and cannot be wildcard")
    return normalized


@dataclass(frozen=True)
class RunScope:
    user_id: str
    matter_id: str
    agent_id: str
    run_id: str

    def __post_init__(self) -> None:
        for field in ("user_id", "matter_id", "agent_id", "run_id"):
            object.__setattr__(self, field, _required(getattr(self, field), field))

    @property
    def namespace(self) -> str:
        raw = json.dumps(
            [self.user_id, self.matter_id, self.agent_id, self.run_id],
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Checkpoint:
    scope: RunScope
    phase: str
    revision: int
    payload: dict[str, Any]


class CheckpointStore:
    """Exact-scope, revisioned local checkpoint boundary.

    Checkpoints are execution state only. They are never legal authority and
    callers must provide already-redacted/minimal payloads.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _path(self, scope: RunScope) -> Path:
        return self.root / f"{scope.namespace}.json"

    def save(self, checkpoint: Checkpoint, *, expected_revision: int | None = None) -> Checkpoint:
        path = self._path(checkpoint.scope)
        current = self.load(checkpoint.scope)
        current_revision = current.revision if current else 0
        if expected_revision is not None and current_revision != expected_revision:
            raise RuntimeError("checkpoint revision conflict")
        if checkpoint.revision != current_revision + 1:
            raise ValueError("checkpoint revision must increase by exactly one")
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "scope_namespace": checkpoint.scope.namespace,
            "phase": _required(checkpoint.phase, "phase"),
            "revision": checkpoint.revision,
            "payload": checkpoint.payload,
            "authority_eligible": False,
        }
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        temp.replace(path)
        return checkpoint

    def load(self, scope: RunScope) -> Checkpoint | None:
        path = self._path(scope)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("scope_namespace") != scope.namespace:
            raise PermissionError("checkpoint scope mismatch")
        if data.get("authority_eligible") is not False:
            raise PermissionError("checkpoint cannot be legal authority")
        return Checkpoint(
            scope=scope,
            phase=_required(data.get("phase", ""), "phase"),
            revision=int(data["revision"]),
            payload=dict(data.get("payload") or {}),
        )

    def delete(self, scope: RunScope) -> bool:
        path = self._path(scope)
        if not path.exists():
            return False
        path.unlink()
        return True


def checkpoint_can_verify_authority(checkpoint: Checkpoint) -> bool:
    return False
