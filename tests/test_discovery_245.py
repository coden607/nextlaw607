from nextlaw607.features.discovery_245 import build

def test_readiness_without_coc_is_flagged():
    x=build(coc_filed=False,readiness_announced=True)
    assert "readiness_validity_review" in x
    assert "coc_gap" in x
