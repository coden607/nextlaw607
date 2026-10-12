from datetime import date

from nextlaw607.authority import (
    AuthorityStatus,
    CitationFirewall,
    LegalAuthority,
    SourceTier,
)


def test_citation_history_must_be_independent_of_authority_source_provider():
    authority = LegalAuthority(
        citation="1 N.Y.3d 1",
        title="People v Example",
        court="NY Court of Appeals",
        jurisdiction="NY",
        decision_date=date(2024, 1, 1),
        source_url="https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        source_tier=SourceTier.OFFICIAL,
        holding="A verified holding.",
        status=AuthorityStatus.GOOD_LAW,
        last_verified_on=date.today(),
        verification_sources=("https://www.courtlistener.com/opinion/123/example/",),
        citation_history_checked_on=date.today(),
        negative_treatment_found=False,
        history_sources=("https://www.nycourts.gov/reporter/3dseries/2024/example.htm",),
    )

    decision = CitationFirewall().verify(authority)

    assert not decision.verified
    assert any("citation history not independent" in reason for reason in decision.reasons)
