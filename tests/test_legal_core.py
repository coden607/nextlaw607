from datetime import date, timedelta
from nextlaw607.authority import AuthorityStatus, CitationFirewall, LegalAuthority, SourceTier
from nextlaw607.encounter import EncounterMode, EncounterSafety
from nextlaw607.live import LiveEncounterEngine
from nextlaw607.research import LegalResearchRequest, ResearchWorkflow
from nextlaw607.sources import SourceRegistry
from nextlaw607.suppression import SuppressionAnalyzer, SuppressionFacts


def auth(**kw):
    base=dict(citation="1 N.Y.3d 1", title="People v Example", court="NY Court of Appeals", jurisdiction="NY", decision_date=date(2024,1,1), source_url="https://nycourts.gov/example", source_tier=SourceTier.OFFICIAL, holding="A verified holding.", status=AuthorityStatus.GOOD_LAW, last_verified_on=date.today(), verification_sources=("https://nycourts.gov/example",), citation_history_checked_on=date.today(), negative_treatment_found=False, history_sources=("https://www.courtlistener.com/opinion/123/example/",))
    base.update(kw); return LegalAuthority(**base)

def test_verified_authority_passes(): assert CitationFirewall().verify(auth()).verified
def test_stale_authority_fails(): assert not CitationFirewall(30).verify(auth(last_verified_on=date.today()-timedelta(days=31))).verified
def test_secondary_only_fails(): assert not CitationFirewall().verify(auth(source_tier=SourceTier.SECONDARY)).verified
def test_unknown_status_fails(): assert not CitationFirewall().verify(auth(status=AuthorityStatus.UNKNOWN)).verified
def test_source_registry_prioritizes_ny_official(): assert SourceRegistry().ordered_for("NY")[0].jurisdiction == "NY" and SourceRegistry().ordered_for("NY")[0].official
def test_research_only_cites_verified():
    result=ResearchWorkflow().evaluate(LegalResearchRequest("rule?","NY"), [auth(), auth(citation="bad", status=AuthorityStatus.UNKNOWN)])
    assert len(result.citable_authorities)==1
def test_prolonged_stop_issue(): assert any(i.code=="prolonged_stop" for i in SuppressionAnalyzer().analyze(SuppressionFacts(traffic_stop=True,traffic_mission_complete=True,additional_detention=True)))
def test_warrantless_search_issue(): assert any(i.code=="warrantless_search" for i in SuppressionAnalyzer().analyze(SuppressionFacts(search_occurred=True)))
def test_consent_scope_issue(): assert any(i.code=="consent_scope" for i in SuppressionAnalyzer().analyze(SuppressionFacts(search_occurred=True,consent=True)))
def test_unsafe_goal_redirects(): assert not EncounterSafety().evaluate_goal("help me resist and run").allowed
def test_search_live_script_preserves_nonconsent(): assert "I do not consent to any search." in LiveEncounterEngine().respond(EncounterMode.SEARCH).say_now
def test_interrogation_invokes_silence_and_lawyer():
    text=" ".join(LiveEncounterEngine().respond(EncounterMode.INTERROGATION).say_now).lower(); assert "remain silent" in text and "lawyer" in text
def test_arrest_script_asks_for_lawyer(): assert any("lawyer" in x.lower() for x in LiveEncounterEngine().respond(EncounterMode.ARREST).say_now)
def test_live_response_preserves_event_details(): assert "officer identifiers" in LiveEncounterEngine().respond(EncounterMode.STREET_STOP).preserve_for_later[0]

from datetime import datetime, timezone
from nextlaw607.procedure import CaseEvent, CriminalCaseState, ProcedureStage

def test_case_state_tracks_procedural_stage_and_next_actions():
    case=CriminalCaseState("m1","NY")
    case.record(CaseEvent(ProcedureStage.ARRAIGNMENT, datetime(2026,9,1,tzinfo=timezone.utc), "Arraignment"))
    assert case.stage is ProcedureStage.ARRAIGNMENT
    assert any("counsel" in x.lower() for x in case.next_actions())

def test_case_state_rejects_out_of_order_events():
    import pytest
    case=CriminalCaseState("m1","NY")
    case.record(CaseEvent(ProcedureStage.ARREST, datetime(2026,9,2,tzinfo=timezone.utc), "Arrest"))
    with pytest.raises(ValueError):
        case.record(CaseEvent(ProcedureStage.INVESTIGATION, datetime(2026,9,1,tzinfo=timezone.utc), "Earlier"))

def test_appearance_ticket_action_does_not_invent_deadline():
    case=CriminalCaseState("m1","NY", stage=ProcedureStage.APPEARANCE_TICKET)
    text=" ".join(case.next_actions()).lower()
    assert "shown on the ticket" in text
    assert "days" not in text

def test_good_law_label_without_fresh_history_review_fails_closed():
    candidate = auth(citation_history_checked_on=None, negative_treatment_found=None)
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("citation history" in reason for reason in decision.reasons)


def test_fresh_negative_history_review_allows_otherwise_verified_authority():
    candidate = auth(
        citation_history_checked_on=date.today(),
        negative_treatment_found=False,
        history_sources=("https://www.courtlistener.com/opinion/123/example/", "https://www.nycourts.gov/reporter/3dseries/2024/example.htm"),
    )
    assert CitationFirewall().verify(candidate).verified


def test_detected_negative_treatment_always_blocks_citation():
    candidate = auth(
        citation_history_checked_on=date.today(),
        negative_treatment_found=True,
        history_sources=("https://www.courtlistener.com/opinion/123/example/",),
    )
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("negative treatment" in reason for reason in decision.reasons)

def test_release_grand_jury_and_plea_stages_have_noninvented_actions():
    for stage, phrase in [
        (ProcedureStage.RELEASE_BAIL_REMAND, "release"),
        (ProcedureStage.GRAND_JURY, "grand jury"),
        (ProcedureStage.PLEA, "plea"),
    ]:
        case = CriminalCaseState("m1", "NY", stage=stage)
        text = " ".join(case.next_actions()).lower()
        assert phrase in text
        assert "within " not in text
        assert "days" not in text

def test_home_entry_without_warrant_consent_or_exigency_flags_issue():
    issues = SuppressionAnalyzer().analyze(SuppressionFacts(home_entry=True))
    assert any(i.code == "home_entry_authority" for i in issues)


def test_protective_sweep_and_plain_view_are_separate_review_issues():
    issues = SuppressionAnalyzer().analyze(SuppressionFacts(home_entry=True, warrant=True, protective_sweep=True, plain_view_seizure=True))
    codes = {i.code for i in issues}
    assert "protective_sweep_scope" in codes
    assert "plain_view_scope" in codes


def test_custodial_questioning_without_miranda_flags_issue():
    issues = SuppressionAnalyzer().analyze(SuppressionFacts(interrogation=True, in_custody=True, police_questioning=True, miranda_given=False))
    assert any(i.code == "miranda_issue" for i in issues)


def test_questioning_after_counsel_request_flags_issue_without_declaring_suppression():
    issues = SuppressionAnalyzer().analyze(SuppressionFacts(interrogation=True, counsel_requested=True, questioning_continued_after_counsel=True))
    issue = next(i for i in issues if i.code == "post_counsel_questioning")
    assert issue.needs_authority_verification
    assert "verify" in issue.summary.lower()


def test_identification_procedure_flags_wade_showup_review_without_outcome_claim():
    issues = SuppressionAnalyzer().analyze(SuppressionFacts(identification_procedure=True))
    assert any(i.code == "identification_procedure" for i in issues)


def test_claimed_official_source_must_match_registered_official_domain():
    candidate = auth(
        source_url="https://example.com/not-official",
        verification_sources=(),
    )
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("official source" in reason for reason in decision.reasons)


def test_repository_copy_can_pass_when_official_text_was_cross_checked():
    candidate = auth(
        source_url="https://www.courtlistener.com/opinion/123/example/",
        source_tier=SourceTier.REPOSITORY,
        verification_sources=("https://www.nycourts.gov/reporter/3dseries/2024/example.htm",),
        history_sources=("https://www.courtlistener.com/opinion/123/example/",),
    )
    assert CitationFirewall().verify(candidate).verified


def test_next_appearance_without_source_fails_closed_in_actions():
    case = CriminalCaseState(
        "m1",
        "NY",
        stage=ProcedureStage.PRETRIAL,
        next_appearance=datetime(2026, 10, 1, tzinfo=timezone.utc),
    )
    text = " ".join(case.next_actions()).lower()
    assert "unverified" in text
    assert "confirm" in text
    assert "2026" not in text


def test_next_appearance_with_source_can_be_safely_surfaced():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    case.set_next_appearance(
        datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
        source="court notice dated 2026-09-20",
        source_kind="court_notice",
    )
    text = " ".join(case.next_actions()).lower()
    assert "2026-10-01" in text
    assert "court notice" in text


def test_citation_history_requires_trusted_research_source_url():
    candidate = auth(history_sources=("reviewed by researcher",))
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("citation history source" in reason for reason in decision.reasons)


def test_citation_history_accepts_registered_repository_source():
    candidate = auth(history_sources=("https://www.courtlistener.com/opinion/123/example/",))
    assert CitationFirewall().verify(candidate).verified


def test_next_appearance_rejects_unclassified_source():
    import pytest
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    with pytest.raises(ValueError):
        case.set_next_appearance(
            datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
            source="friend texted me",
        )


def test_next_appearance_accepts_court_or_counsel_source_kinds():
    for source_kind in ("court_notice", "docket", "counsel_confirmation"):
        case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
        case.set_next_appearance(
            datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
            source="verified source",
            source_kind=source_kind,
        )
        assert "Verified next appearance" in " ".join(case.next_actions())


def test_source_registry_distinguishes_citation_history_from_statute_text():
    registry = SourceRegistry()
    supports = getattr(registry, "supports", None)
    assert supports is not None, "SourceRegistry.supports is required"
    assert supports("https://legislation.nysenate.gov/laws/CPL/1.20", "primary_text", "NY")
    assert not supports("https://legislation.nysenate.gov/laws/CPL/1.20", "citation_history", "NY")
    assert supports("https://www.courtlistener.com/opinion/123/example/", "citation_history", "NY")


def test_citation_firewall_rejects_registered_source_without_history_capability():
    candidate = auth(history_sources=("https://legislation.nysenate.gov/laws/CPL/1.20",))
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("citation history source" in reason for reason in decision.reasons)


def test_case_deadline_requires_classified_provenance_and_surfaces_source():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)
    add_deadline = getattr(case, "add_deadline", None)
    assert add_deadline is not None, "CriminalCaseState.add_deadline is required"
    add_deadline(
        "motion filing",
        datetime(2026, 10, 15, 17, 0, tzinfo=timezone.utc),
        source="court scheduling order dated 2026-09-25",
        source_kind="court_notice",
    )
    text = " ".join(case.next_actions()).lower()
    assert "2026-10-15" in text
    assert "motion filing" in text
    assert "court scheduling order" in text


def test_case_deadline_rejects_unclassified_source_and_sorts_chronologically():
    import pytest

    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    add_deadline = getattr(case, "add_deadline", None)
    assert add_deadline is not None, "CriminalCaseState.add_deadline is required"
    with pytest.raises(ValueError):
        add_deadline(
            "unknown deadline",
            datetime(2026, 11, 1, tzinfo=timezone.utc),
            source="someone said so",
            source_kind="friend_message",
        )
    add_deadline(
        "later filing",
        datetime(2026, 11, 10, tzinfo=timezone.utc),
        source="counsel confirmation",
        source_kind="counsel_confirmation",
    )
    add_deadline(
        "earlier filing",
        datetime(2026, 11, 2, tzinfo=timezone.utc),
        source="docket entry",
        source_kind="docket",
    )
    assert [deadline.title for deadline in case.deadlines] == ["earlier filing", "later filing"]


def test_verification_sources_must_be_registered_primary_text_urls():
    candidate = auth(verification_sources=("official",))
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert any("verification source" in reason for reason in decision.reasons)
