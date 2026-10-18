from datetime import date
from nextlaw607.features.rule_versions import RuleVersion, select

def test_rule_version_selects_exact_period():
    a=RuleVersion("old",date(2020,1,1),date(2024,1,1),"22 NYCRR")
    b=RuleVersion("new",date(2024,1,1),None,"22 NYCRR")
    assert select([a,b],date(2025,1,1)).id=="new"
