from datetime import datetime, timezone

import pytest

from nextlaw607.procedure import CriminalCaseState, DeadlineKind, ProcedureStage


def test_typed_deadline_kind_is_preserved_and_surfaced_without_inventing_dates():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)
    case.add_deadline(
        "omnibus motion filing",
        datetime(2026, 10, 15, 17, 0, tzinfo=timezone.utc),
        source="court scheduling order dated 2026-09-25",
        source_kind="court_notice",
        kind=DeadlineKind.MOTION,
    )

    assert case.deadlines[0].kind is DeadlineKind.MOTION
    text = " ".join(case.next_actions()).lower()
    assert "motion deadline" in text
    assert "2026-10-15" in text
    assert "court scheduling order" in text


def test_untyped_deadline_remains_general_for_backward_compatible_fail_closed_storage():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.add_deadline(
        "source-backed filing",
        datetime(2026, 11, 2, tzinfo=timezone.utc),
        source="docket entry",
        source_kind="docket",
    )

    assert case.deadlines[0].kind is DeadlineKind.GENERAL
    assert "general deadline" in " ".join(case.next_actions()).lower()


def test_statutory_deadline_rejects_free_form_source_without_official_primary_text():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)

    with pytest.raises(ValueError, match="statutory/rule deadline requires official primary-text source URL"):
        case.add_deadline(
            "statutory motion deadline",
            datetime(2026, 10, 20, tzinfo=timezone.utc),
            source="CPL 255.20",
            source_kind="statute",
            kind=DeadlineKind.MOTION,
        )


def test_statutory_deadline_accepts_registered_official_primary_text_source():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)
    source_url = "https://legislation.nysenate.gov/laws/CPL/255.20"

    case.add_deadline(
        "statutory motion deadline",
        datetime(2026, 10, 20, tzinfo=timezone.utc),
        source="CPL 255.20",
        source_kind="statute",
        source_url=source_url,
        kind=DeadlineKind.MOTION,
    )

    assert case.deadlines[0].source_url == source_url
