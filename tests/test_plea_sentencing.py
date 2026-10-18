import pytest
from nextlaw607.features.plea_sentencing import build

def test_unknown_conviction_offense_fails_closed():
    with pytest.raises(ValueError): build(plea_offer=False,conviction_offense_known=False,predicate_status_known=True)

def test_unknown_predicate_is_flagged():
    assert "predicate_status_gap" in build(plea_offer=True,conviction_offense_known=True,predicate_status_known=False)
