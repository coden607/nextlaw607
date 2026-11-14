import pytest
from nextlaw607.features.motion_outline import generate

def test_motion_outline_rejects_unverified_authority():
    with pytest.raises(ValueError):
        generate(issue="suppression",facts=["fact"],authorities=[{"citation":"X","source":"s","verified":False}])

def test_motion_outline_uses_only_verified_authority():
    out=generate(issue="suppression",facts=["fact"],authorities=[{"citation":"A","source":"s","verified":True},{"citation":"B","source":"s","verified":False}])
    assert out["authorities"]==("A",)
