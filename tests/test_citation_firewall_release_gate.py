from datetime import date, timedelta

from nextlaw607.authority import AuthorityStatus, CitationFirewall, LegalAuthority, SourceTier
from nextlaw607.research import LegalResearchRequest, ResearchWorkflow


def _authority(**overrides):
    values = {
        "citation": "1 N.Y.3d 1",
        "title": "People v Example",
        "court": "NY Court of Appeals",
        "jurisdiction": "NY",
        "decision_date": date(2024, 1, 1),
        "source_url": "https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        "source_tier": SourceTier.OFFICIAL,
        "holding": "A verified holding.",
        "status": AuthorityStatus.GOOD_LAW,
        "last_verified_on": date.today(),
        "verification_sources": ("https://www.nycourts.gov/reporter/3dseries/2024/example.htm",),
        "citation_history_checked_on": date.today(),
        "negative_treatment_found": False,
        "history_sources": ("https://www.courtlistener.com/opinion/123/example/",),
    }
    values.update(overrides)
    return LegalAuthority(**values)


def test_release_gate_accepts_only_fresh_independently_checked_primary_authority():
    decision = CitationFirewall().verify(_authority())
    assert decision.verified
    assert decision.label == "VERIFIED"


def test_release_gate_fails_closed_on_negative_treatment_even_with_good_law_label():
    decision = CitationFirewall().verify(_authority(negative_treatment_found=True))
    assert not decision.verified
    assert decision.label == "UNVERIFIED — DO NOT CITE"
    assert "negative treatment found" in decision.reasons


def test_release_gate_fails_closed_when_history_review_is_stale():
    decision = CitationFirewall(30).verify(
        _authority(citation_history_checked_on=date.today() - timedelta(days=31))
    )
    assert not decision.verified
    assert "citation history review stale" in decision.reasons


def test_release_gate_fails_closed_when_history_provider_is_not_independent():
    official = "https://www.nycourts.gov/reporter/3dseries/2024/example.htm"
    decision = CitationFirewall().verify(_authority(history_sources=(official,)))
    assert not decision.verified
    assert "citation history not independent of text verification" in decision.reasons


def test_release_gate_never_allows_unverified_candidate_into_citable_results():
    verified = _authority()
    model_like_candidate = _authority(
        citation="model-output",
        source_url="https://example.com/generated",
        source_tier=SourceTier.REPOSITORY,
        verification_sources=(),
        history_sources=(),
        negative_treatment_found=None,
        status=AuthorityStatus.UNKNOWN,
    )
    result = ResearchWorkflow().evaluate(
        LegalResearchRequest("rule?", "NY"),
        [verified, model_like_candidate],
    )
    assert len(result.citable_authorities) == 1
    assert result.citable_authorities[0].authority == verified
    assert result.citable_authorities[0].verification.verified
