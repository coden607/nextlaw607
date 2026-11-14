from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Iterable


class CoverageState(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING = "missing"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CorpusCoverageTarget:
    source_id: str
    jurisdiction: str
    document_class: str
    start_date: date
    end_date: date | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.jurisdiction.strip():
            raise ValueError("jurisdiction is required")
        if not self.document_class.strip():
            raise ValueError("document_class is required")
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date cannot precede start_date")


@dataclass(frozen=True)
class CorpusCoverageObservation:
    source_id: str
    jurisdiction: str
    document_class: str
    earliest_date: date | None
    latest_date: date | None
    expected_documents: int | None
    indexed_documents: int
    last_successful_ingest: date | None

    def __post_init__(self) -> None:
        if self.indexed_documents < 0:
            raise ValueError("indexed_documents cannot be negative")
        if self.expected_documents is not None and self.expected_documents < 0:
            raise ValueError("expected_documents cannot be negative")
        if (
            self.earliest_date is not None
            and self.latest_date is not None
            and self.latest_date < self.earliest_date
        ):
            raise ValueError("latest_date cannot precede earliest_date")


@dataclass(frozen=True)
class CorpusCoverageResult:
    target: CorpusCoverageTarget
    state: CoverageState
    coverage_ratio: float | None
    reasons: tuple[str, ...]


def evaluate_corpus_coverage(
    target: CorpusCoverageTarget,
    observation: CorpusCoverageObservation | None,
    *,
    today: date,
    stale_after_days: int = 7,
) -> CorpusCoverageResult:
    if stale_after_days < 0:
        raise ValueError("stale_after_days cannot be negative")
    if observation is None:
        return CorpusCoverageResult(
            target=target,
            state=CoverageState.MISSING,
            coverage_ratio=0.0,
            reasons=("no coverage observation",),
        )

    identity = (target.source_id, target.jurisdiction, target.document_class)
    observed_identity = (
        observation.source_id,
        observation.jurisdiction,
        observation.document_class,
    )
    if identity != observed_identity:
        return CorpusCoverageResult(
            target=target,
            state=CoverageState.UNKNOWN,
            coverage_ratio=None,
            reasons=("coverage observation identity mismatch",),
        )

    reasons: list[str] = []
    ratio: float | None = None
    if observation.expected_documents is not None:
        if observation.expected_documents == 0:
            ratio = 1.0 if observation.indexed_documents == 0 else None
        else:
            ratio = min(observation.indexed_documents / observation.expected_documents, 1.0)
            if observation.indexed_documents < observation.expected_documents:
                reasons.append("indexed document count below expected count")
    else:
        reasons.append("expected document count unknown")

    if observation.earliest_date is None or observation.earliest_date > target.start_date:
        reasons.append("coverage does not reach target start date")

    target_end = target.end_date or today
    if observation.latest_date is None or observation.latest_date < target_end:
        reasons.append("coverage does not reach target end date")

    if observation.last_successful_ingest is None:
        reasons.append("no successful ingestion timestamp")
    elif observation.last_successful_ingest > today:
        reasons.append("successful ingestion timestamp is in the future")
    elif (today - observation.last_successful_ingest).days > stale_after_days:
        reasons.append("ingestion freshness is stale")

    if not reasons:
        state = CoverageState.COMPLETE
    elif observation.indexed_documents == 0:
        state = CoverageState.MISSING
    else:
        state = CoverageState.PARTIAL

    return CorpusCoverageResult(
        target=target,
        state=state,
        coverage_ratio=ratio,
        reasons=tuple(reasons),
    )


def coverage_summary(results: Iterable[CorpusCoverageResult]) -> dict[str, int]:
    summary = {state.value: 0 for state in CoverageState}
    for result in results:
        summary[result.state.value] += 1
    return summary
