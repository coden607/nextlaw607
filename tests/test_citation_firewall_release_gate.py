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
        "source_url": "https://nycourts.gov/example",
        "source_tier": SourceTier.OFFICIAL,
        "holding": "A verified holding.",
        "status": AuthorityStatus.GOOD_LAW,
        "last_verified_on": date.today(),
        "verification_sources": ("https://nycourts.gov/example",),
        "citation_history_checked_on": date.today(),
        "negative_treatment_found": False,
        "history_sources": ("https://www.courtlistener.com/opinion/123/example/",),
    }
    values.update(overrides)
    return LegalAuthority(**values)


def test_release_gate_accepts_fresh_primary_authority_with_independent_history_review():
    assert CitationFirewall().verify(_authority()).verified


def test_release_gate_rejects_negative_treatment():
    decision = CitationFirewall().verify(_authority(negative_treatment_found=True))
    assert not decision.verified
    assert any("negative treatment" in reason for reason in decision.reasons)


def test_release_gate_rejects_stale_primary_text_verification():
    decision = CitationFirewall(30).verify(
        _authority(last_verified_on=date.today() - timedelta(days=31))
    )
    assert not decision.verified
    assert any("verification stale" in reason for reason in decision.reasons)


def test_release_gate_rejects_unregistered_model_like_source():
    candidate = _authority(
        citation="model-output",
        source_url="https://example.com/generated",
        source_tier=SourceTier.REPOSITORY,
        verification_sources=(),
        history_sources=(),
        negative_treatment_found=None,
        status=AuthorityStatus.UNKNOWN,
    )
    decision = CitationFirewall().verify(candidate)
    assert not decision.verified
    assert decision.label == "UNVERIFIED — DO NOT CITE"


def test_release_gate_research_workflow_only_surfaces_verified_candidates():
    result = ResearchWorkflow().evaluate(
        LegalResearchRequest("rule?", "NY"),
        [_authority(), _authority(citation="bad", status=AuthorityStatus.UNKNOWN)],
    )
    assert len(result.citable_authorities) == 1
    assert result.citable_authorities[0].verification.verified
