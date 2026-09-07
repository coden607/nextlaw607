from datetime import datetime, timezone

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
