from nextlaw607.features.constitutional_interaction import classify

def test_dual_sovereign_labels_are_explicit():
    assert classify(source="us_supreme_court",issue_basis="both")=="federal_controlling"
    assert classify(source="ny_court_of_appeals",issue_basis="state",state_protection_broader=True)=="state_controlling_broader"
