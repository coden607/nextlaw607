import pytest
from nextlaw607.features.bail_workflow import build

def test_bail_requires_verified_threshold():
    with pytest.raises(ValueError): build(qualifying_offense=None,risk_of_flight_facts=False,current_order=False)

def test_existing_order_adds_review_gate():
    assert "changed_circumstances_or_review_basis" in build(qualifying_offense=True,risk_of_flight_facts=False,current_order=True)
