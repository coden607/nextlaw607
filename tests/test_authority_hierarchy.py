from nextlaw607.features.authority_hierarchy import score_authority

def test_higher_court_outscores_trial_court():
    assert score_authority(court="ny_court_of_appeals", jurisdiction_match=True) > score_authority(court="ny_trial_court", jurisdiction_match=True)

def test_stale_authority_is_penalized():
    current = score_authority(court="ny_appellate_division", jurisdiction_match=True, current=True)
    stale = score_authority(court="ny_appellate_division", jurisdiction_match=True, current=False)
    assert current - stale == 40
