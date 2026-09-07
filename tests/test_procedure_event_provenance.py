from datetime import datetime, timezone

import pytest

from nextlaw607.procedure import CaseEvent, CriminalCaseState, ProcedureStage


def test_record_rejects_event_source_without_classified_source_kind():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court minute entry",
    )

    with pytest.raises(ValueError, match="event source requires a trusted source kind"):
        case.record(event)


def test_record_rejects_event_source_kind_without_source():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source_kind="docket",
    )

    with pytest.raises(ValueError, match="event source kind requires a source"):
        case.record(event)


def test_record_accepts_classified_event_provenance():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court docket entry 42",
        source_kind="docket",
    )

    case.record(event)

    assert case.events[-1].source == "court docket entry 42"
    assert case.events[-1].source_kind == "docket"
