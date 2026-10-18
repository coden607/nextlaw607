from nextlaw607.features.citator_schema import TreatmentEvidence
from nextlaw607.features.citator_review import build_queue

def test_uncertain_treatment_is_queued():
    items=[TreatmentEvidence("a","followed",True,.99,"s1"),TreatmentEvidence("b","limited",False,.95,"s2")]
    assert [x.authority_id for x in build_queue(items)]==["b"]
