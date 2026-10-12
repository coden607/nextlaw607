from datetime import datetime, timezone

from nextlaw607.procedure import CriminalCaseState, ProcedureStage


def test_source_backed_appearance_without_verification_is_not_labeled_verified():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.set_next_appearance(
        datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
        source="court notice dated 2026-09-20",
        source_kind="court_notice",
    )

    text = " ".join(case.next_actions()).lower()

    assert "2026-10-01" in text
    assert "source-backed next appearance" in text
    assert "verified next appearance" not in text
    assert "verify before relying" in text


def test_explicitly_verified_appearance_keeps_verified_label():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.set_next_appearance(
        datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
        source="court notice dated 2026-09-20",
        source_kind="court_notice",
        source_url="https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        verified_at=datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        as_of=datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
    )

    text = " ".join(case.next_actions()).lower()

    assert "verified next appearance" in text
    assert "2026-10-01" in text
