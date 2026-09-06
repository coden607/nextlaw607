from datetime import date, datetime, timedelta, timezone

from nextlaw607.authority import AuthorityStatus, CitationFirewall, LegalAuthority, SourceTier
from nextlaw607.procedure import CriminalCaseState, ProcedureStage


def _authority(**changes):
    today = date.today()
    base = dict(
        citation="1 N.Y.3d 1",
        title="People v Example",
        court="NY Court of Appeals",
        jurisdiction="NY",
        decision_date=date(2024, 1, 1),
        source_url="https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        source_tier=SourceTier.OFFICIAL,
        holding="Verified holding.",
        status=AuthorityStatus.GOOD_LAW,
        last_verified_on=today,
        verification_sources=("https://www.nycourts.gov/reporter/3dseries/2024/example.htm",),
        citation_history_checked_on=today,
        negative_treatment_found=False,
        history_sources=("https://www.courtlistener.com/opinion/123/example/",),
    )
    base.update(changes)
    return LegalAuthority(**base)


def test_citation_firewall_rejects_future_verification_dates():
    today = date(2026, 9, 6)
    candidate = _authority(
        last_verified_on=today + timedelta(days=1),
        citation_history_checked_on=today + timedelta(days=1),
    )
    decision = CitationFirewall().verify(candidate, today=today)
    assert not decision.verified
    assert "verification date is in the future" in decision.reasons
    assert "citation history review date is in the future" in decision.reasons


def test_citation_firewall_rejects_verification_before_decision():
    candidate = _authority(
        decision_date=date(2026, 9, 1),
        last_verified_on=date(2026, 8, 31),
        citation_history_checked_on=date(2026, 8, 31),
    )
    decision = CitationFirewall().verify(candidate, today=date(2026, 9, 6))
    assert not decision.verified
    assert "verification predates decision" in decision.reasons
    assert "citation history review predates decision" in decision.reasons


def test_deadline_actions_label_overdue_without_inventing_deadlines():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)
    case.add_deadline(
        "motion filing",
        datetime(2026, 9, 5, 17, 0, tzinfo=timezone.utc),
        source="court scheduling order",
        source_kind="court_notice",
    )
    actions = case.next_actions(as_of=datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc))
    text = " ".join(actions).lower()
    assert "overdue source-backed deadline" in text
    assert "court scheduling order" in text


def test_deadline_actions_keep_future_source_backed_deadline_upcoming():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.add_deadline(
        "court appearance filing",
        datetime(2026, 9, 10, 9, 0, tzinfo=timezone.utc),
        source="docket entry",
        source_kind="docket",
    )
    actions = case.next_actions(as_of=datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc))
    text = " ".join(actions).lower()
    assert "upcoming source-backed deadline" in text
    assert "docket entry" in text
