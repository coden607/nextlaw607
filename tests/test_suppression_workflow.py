import pytest
from nextlaw607.features.suppression_workflow import build

def test_statement_workflow_contains_core_gates():
    x=build("statement")
    assert "burden_map" in x and "voluntariness" in x and "adverse_authority" in x

def test_unknown_type_fails_closed():
    with pytest.raises(ValueError): build("other")
