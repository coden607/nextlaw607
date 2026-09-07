from datetime import date, datetime, timedelta, timezone

import pytest

from nextlaw607.authority import AuthorityStatus, CitationFirewall, LegalAuthority, SourceTier
from nextlaw607.procedure import CaseEvent, CriminalCaseState, ProcedureStage


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


def test_citation_firewall_rejects_history_review_older_than_latest_text_verification():
    today = date(2026, 9, 7)
    candidate = _authority(
        last_verified_on=date(2026, 9, 7),
        citation_history_checked_on=date(2026, 9, 6),
    )
    decision = CitationFirewall().verify(candidate, today=today)
    assert not decision.verified
    assert "citation history review predates latest text verification" in decision.reasons


def test_citation_firewall_rejects_duplicate_citation_history_sources():
    today = date(2026, 9, 6)
    candidate = _authority(
        last_verified_on=today,
        citation_history_checked_on=today,
        history_sources=(
            "https://www.courtlistener.com/opinion/123/example/",
            "https://courtlistener.com/opinion/123/example/?type=o",
        ),
    )
    decision = CitationFirewall().verify(candidate, today=today)
    assert not decision.verified
    assert "citation history sources are not independent" in decision.reasons


def test_citation_firewall_rejects_same_registered_provider_across_subdomains():
    today = date(2026, 9, 6)
    candidate = _authority(
        last_verified_on=today,
        citation_history_checked_on=today,
        history_sources=(
            "https://www.courtlistener.com/opinion/123/example/",
            "https://api.courtlistener.com/api/rest/v3/opinions/123/",
        ),
    )
    decision = CitationFirewall().verify(candidate, today=today)
    assert not decision.verified
    assert "citation history sources are not independent" in decision.reasons


def test_citation_history_must_be_independent_of_primary_text_verification_provider():
    today = date(2026, 9, 7)
    candidate = _authority(
        last_verified_on=today,
        citation_history_checked_on=today,
        verification_sources=(
            "https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        ),
        history_sources=(
            "https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        ),
    )
    decision = CitationFirewall().verify(candidate, today=today)
    assert not decision.verified
    assert "citation history not independent of text verification" in decision.reasons


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


def test_past_dated_verified_appearance_requires_current_recheck():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.set_next_appearance(
        datetime(2026, 9, 5, 9, 0, tzinfo=timezone.utc),
        source="court notice dated 2026-09-01",
        source_kind="court_notice",
    )
    actions = case.next_actions(as_of=datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc))
    text = " ".join(actions).lower()
    assert "past-dated verified appearance" in text
    assert "re-check current court or counsel source" in text
    assert "court notice dated 2026-09-01" in text


def test_next_appearance_rejects_future_source_verification_timestamp():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    with pytest.raises(ValueError, match="appearance source verification is in the future"):
        case.set_next_appearance(
            datetime(2026, 9, 12, 9, 0, tzinfo=timezone.utc),
            source="court notice",
            source_kind="court_notice",
            verified_at=datetime(2026, 9, 8, 9, 0, tzinfo=timezone.utc),
            as_of=datetime(2026, 9, 7, 9, 0, tzinfo=timezone.utc),
        )


def test_next_appearance_rejects_date_before_source_verification():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    with pytest.raises(ValueError, match="appearance predates source verification"):
        case.set_next_appearance(
            datetime(2026, 9, 8, 9, 0, tzinfo=timezone.utc),
            source="court notice",
            source_kind="court_notice",
            verified_at=datetime(2026, 9, 9, 9, 0, tzinfo=timezone.utc),
        )


def test_record_rejects_event_timestamp_after_explicit_as_of():
    case = CriminalCaseState("m1", "NY")
    event = CaseEvent(
        stage=ProcedureStage.ARRAIGNMENT,
        occurred_at=datetime(2026, 9, 7, 9, 0, tzinfo=timezone.utc),
        title="arraignment",
        source="court minute entry",
    )
    with pytest.raises(ValueError, match="event timestamp is in the future"):
        case.record(event, as_of=datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc))
