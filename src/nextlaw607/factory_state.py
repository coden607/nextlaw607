from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FactoryStage(str, Enum):
    PRD = "prd"
    ARCHITECTURE = "architecture"
    IMPLEMENT = "implement"
    TEST = "test"
    REVIEW = "review"
    VERIFY = "verify"
    COMPLETE = "complete"


_ALLOWED: dict[FactoryStage, set[FactoryStage]] = {
    FactoryStage.PRD: {FactoryStage.ARCHITECTURE},
    FactoryStage.ARCHITECTURE: {FactoryStage.IMPLEMENT},
    FactoryStage.IMPLEMENT: {FactoryStage.TEST},
    FactoryStage.TEST: {FactoryStage.IMPLEMENT, FactoryStage.REVIEW},
    FactoryStage.REVIEW: {FactoryStage.IMPLEMENT, FactoryStage.VERIFY},
    FactoryStage.VERIFY: {FactoryStage.IMPLEMENT, FactoryStage.COMPLETE},
    FactoryStage.COMPLETE: set(),
}


@dataclass(frozen=True)
class FactoryState:
    stage: FactoryStage = FactoryStage.PRD
    revision: int = 0

    def transition(self, target: FactoryStage) -> "FactoryState":
        if target not in _ALLOWED[self.stage]:
            raise ValueError(f"invalid factory transition: {self.stage.value}->{target.value}")
        return FactoryState(stage=target, revision=self.revision + 1)
