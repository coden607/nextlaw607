from __future__ import annotations

import pytest

from nextlaw607.research import LegalResearchRequest


def test_research_request_defaults_to_criminal_primary_scope():
    request = LegalResearchRequest("What law controls?", "NY")
    assert request.practice == "criminal"
    assert request.criminal_nexus is False


def test_ancillary_law_is_allowed_with_criminal_nexus():
    request = LegalResearchRequest(
        "Is CPLR habeas corpus available for this criminal detention?",
        "NY",
        practice="civil",
        criminal_nexus=True,
    )
    assert request.practice == "civil"
    assert request.criminal_nexus is True


def test_unrelated_noncriminal_research_fails_closed():
    with pytest.raises(ValueError, match="criminal-centered"):
        LegalResearchRequest("standalone contract question", "NY", practice="civil")
