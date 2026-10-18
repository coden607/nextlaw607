from datetime import date
from nextlaw607.features.statute_versions import StatuteVersion, select, lineage

def test_select_and_lineage():
    a=StatuteVersion("a",date(2020,1,1),date(2022,1,1))
    b=StatuteVersion("b",date(2022,1,1),None,"a")
    assert select([a,b],date(2023,1,1)).id=="b"
    assert lineage([a,b],"b")==("b","a")
