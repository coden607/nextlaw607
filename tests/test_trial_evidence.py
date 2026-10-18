import pytest
from nextlaw607.features.trial_evidence import build

def test_trial_evidence_preserves_gaps():
    row=build([{"name":"bodycam","foundation":False}])[0]
    assert row["objection"]=="unassessed" and row["provenance"]=="missing"

def test_blank_item_fails():
    with pytest.raises(ValueError): build([{}])
