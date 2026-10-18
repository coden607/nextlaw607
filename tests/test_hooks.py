import pytest

from nextlaw607.hooks import HookEnforcementBus, HookEvent, HookResult


def test_hooks_allow_when_all_pass():
    bus = HookEnforcementBus()
    bus.register(HookEvent.PRE_TOOL, lambda ctx: HookResult(True))
    bus.enforce(HookEvent.PRE_TOOL, {"tool": "courtlistener"})


def test_hooks_fail_closed_on_denial():
    bus = HookEnforcementBus()
    bus.register(HookEvent.PRE_MODEL, lambda ctx: HookResult(False, "unverified context"))
    with pytest.raises(PermissionError, match="unverified context"):
        bus.enforce(HookEvent.PRE_MODEL, {"task": "legal-synthesis"})
