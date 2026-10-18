from nextlaw607.features.adverse_authority import identify, research_complete

def test_identifies_negative_treatment():
    rows=[{"id":"a","treatment":"limited"},{"id":"b","treatment":"followed"}]
    assert [r["id"] for r in identify(rows)] == ["a"]

def test_completion_requires_adverse_pass():
    assert not research_complete([{"id":"a"}], adverse_pass_ran=False)
