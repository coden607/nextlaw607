from nextlaw607.features.evidence_inventory import digest, audit

def test_inventory_detects_missing_and_duplicate():
    h=digest(b"x")
    out=audit([{"type":"bodycam","sha256":h},{"type":"bodycam","sha256":h}],["bodycam","dispatch"])
    assert out["missing_types"]==("dispatch",)
    assert out["duplicate_hashes"]==(h,)
