from nextlaw607.features.grand_jury_workflow import build

def test_grand_jury_gaps_are_explicit():
    x=build(indictment_present=True,grand_jury_minutes_available=False,preservation_known=False)
    assert "minutes_access_or_review_gap" in x and "preservation_gap" in x
