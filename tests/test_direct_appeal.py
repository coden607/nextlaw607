from nextlaw607.features.direct_appeal import map_issues

def test_preservation_requires_objection_and_ruling():
    rows=map_issues([{"issue":"hearsay","objection":True,"ruling":False}])
    assert rows[0]["preserved"] is False
    assert rows[0]["standard_of_review"]=="unresolved"
