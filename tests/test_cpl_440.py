from nextlaw607.features.cpl_440 import classify_claims

def test_440_separates_record_and_extra_record():
    rows=classify_claims([{"claim":"iac","record_support":True,"extra_record_support":True},{"claim":"new evidence","extra_record_support":True}])
    assert [r["lane"] for r in rows]==["mixed","extra_record"]
