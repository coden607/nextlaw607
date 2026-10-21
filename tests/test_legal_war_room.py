from nextlaw607.features.legal_war_room import dispatch

def test_dispatch_suppression_is_adversarial():
    plan = dispatch("suppression of statement")
    assert "suppression" in plan.stages
    assert "adverse-authority" in plan.stages
    assert plan.requires_verified_authority is True

def test_dispatch_rejects_blank():
    try:
        dispatch("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("blank issue must fail closed")
