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


def test_record_rejects_unverified_court_event_with_unregistered_source_url():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court docket entry 42",
        source_kind="docket",
        source_url="https://example.com/not-a-court-docket",
    )

    with pytest.raises(ValueError, match="court event requires official procedure source URL"):
        case.record(event)


def test_record_preserves_later_verification_of_historical_event():
    case = CriminalCaseState("m1", "NY")
    verified_at = datetime(2026, 9, 7, 10, 0, tzinfo=timezone.utc)
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="counsel confirmed arraignment",
        source_kind="counsel_confirmation",
        verified_at=verified_at,
    )

    case.record(event, as_of=verified_at)

    assert case.events[-1].verified_at == verified_at


def test_record_rejects_future_event_source_verification():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="counsel confirmed arraignment",
        source_kind="counsel_confirmation",
        verified_at=datetime(2026, 9, 8, 10, 0, tzinfo=timezone.utc),
    )

    with pytest.raises(ValueError, match="event source verification is in the future"):
        case.record(event, as_of=datetime(2026, 9, 7, 10, 0, tzinfo=timezone.utc))


def test_verified_docket_event_requires_official_procedure_source_url():
    case = CriminalCaseState("m1", "NY")
    verified_at = datetime(2026, 9, 7, 10, 0, tzinfo=timezone.utc)
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court docket entry 42",
        source_kind="docket",
        verified_at=verified_at,
    )

    with pytest.raises(ValueError, match="verified court event requires official procedure source URL"):
        case.record(event, as_of=verified_at)


def test_verified_docket_event_accepts_and_preserves_official_procedure_source_url():
    case = CriminalCaseState("m1", "NY")
    verified_at = datetime(2026, 9, 7, 10, 0, tzinfo=timezone.utc)
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court docket entry 42",
        source_kind="docket",
        source_url="https://www.nycourts.gov/courthelp/Criminal/index.shtml",
        verified_at=verified_at,
    )

    case.record(event, as_of=verified_at)

    assert case.events[-1].source_url == "https://www.nycourts.gov/courthelp/Criminal/index.shtml"
