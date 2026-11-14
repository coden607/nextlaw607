import pytest
from nextlaw607.features.probation_restitution import build

def test_restitution_workflow_flags_missing_financial_record():
    x=build(violation_type="restitution",restitution_balance_known=False,ability_to_pay_record=False)
    assert "restitution_balance_gap" in x and "ability_to_pay_record_gap" in x

def test_unknown_violation_fails():
    with pytest.raises(ValueError): build(violation_type="x",restitution_balance_known=True,ability_to_pay_record=True)
