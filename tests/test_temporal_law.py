from datetime import date
from nextlaw607.features.temporal_law import LawVersion, applies, select_applicable

def test_temporal_boundaries_are_half_open():
    v = LawVersion("x", date(2025,1,1), date(2026,1,1))
    assert applies(v, date(2025,1,1))
    assert not applies(v, date(2026,1,1))

def test_ambiguous_version_fails_closed():
    versions = [LawVersion("a", date(2025,1,1)), LawVersion("b", date(2025,1,1))]
    try:
        select_applicable(versions, date(2025,2,1))
    except ValueError:
        pass
    else:
        raise AssertionError("ambiguous versions must fail")
