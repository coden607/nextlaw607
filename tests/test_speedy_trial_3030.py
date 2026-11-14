import pytest
from datetime import date
from nextlaw607.features.speedy_trial_3030 import Period, chargeable_days

def test_chargeable_days_excludes_marked_periods():
    rows=[Period(date(2026,1,1),date(2026,1,11)),Period(date(2026,1,11),date(2026,1,21),True,"motion")]
    assert chargeable_days(rows)==10

def test_invalid_period_fails():
    with pytest.raises(ValueError): chargeable_days([Period(date(2026,2,1),date(2026,1,1))])
