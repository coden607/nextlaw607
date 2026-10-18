import pytest
from nextlaw607.features.citator_schema import TreatmentEvidence

def test_treatment_requires_valid_confidence_and_provenance():
    x=TreatmentEvidence("a","limited",True,0.9,"opinion-1")
    assert x.explicit
    with pytest.raises(ValueError):
        TreatmentEvidence("a","limited",True,1.2,"opinion-1")
