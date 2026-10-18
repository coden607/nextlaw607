from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .execution_state import Checkpoint, CheckpointStore, RunScope


@dataclass(frozen=True)
class ResumeState:
    phase: str
    revision: int
    payload: dict[str, Any]


class InterruptResumeCoordinator:
    def __init__(self, store: CheckpointStore) -> None:
        self.store = store

    def checkpoint(
        self,
        scope: RunScope,
        *,
        phase: str,
        payload: dict[str, Any],
        expected_revision: int,
    ) -> ResumeState:
        checkpoint = Checkpoint(
            scope=scope,
            phase=phase,
            revision=expected_revision + 1,
            payload=dict(payload),
        )
        self.store.save(checkpoint, expected_revision=expected_revision)
        return ResumeState(phase, checkpoint.revision, dict(payload))

    def resume(self, scope: RunScope) -> ResumeState | None:
        checkpoint = self.store.load(scope)
        if checkpoint is None:
            return None
        return ResumeState(
            phase=checkpoint.phase,
            revision=checkpoint.revision,
            payload=dict(checkpoint.payload),
        )
