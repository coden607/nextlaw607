from __future__ import annotations

import pytest

from nextlaw607.research import LegalResearchRequest


def test_research_request_defaults_to_criminal_scope():
    request = LegalResearchRequest("What law controls?", "NY")
    assert request.practice == "criminal"


def test_noncriminal_research_request_fails_closed():
    with pytest.raises(ValueError, match="criminal-law research"):
        LegalResearchRequest("contract question", "NY", practice="civil")
