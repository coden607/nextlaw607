from __future__ import annotations

import json

from nextlaw607.continuity_runtime import (
    ContinuityRouter,
    ContinuityState,
    RouteRequest,
    RoutingLedger,
)


def test_deterministic_classes_use_zero_tokens_when_jev_is_unavailable():
    router = ContinuityRouter(runtime_state=ContinuityState.UNAVAILABLE)
    decision = router.decide(RouteRequest("classification"))
    assert decision.route == "deterministic"
    assert decision.budget_class == "zero-token"
    assert decision.reason_code == "deterministic-fallback"
    assert decision.authority_eligible is False


def test_ready_jev_can_choose_only_safe_low_cost_routes():
    router = ContinuityRouter(
        runtime_state=ContinuityState.READY,
        jev_decide=lambda task: "local_free",
    )
    decision = router.decide(RouteRequest("routing"))
    assert decision.route == "local_free"
    assert decision.reason_code == "jev"
    assert decision.authority_eligible is False


def test_invalid_or_failed_jev_fails_to_deterministic_not_premium():
    router = ContinuityRouter(
        runtime_state=ContinuityState.READY,
        jev_decide=lambda task: "premium",
    )
    decision = router.decide(RouteRequest("guardrail"))
    assert decision.route == "deterministic"
    assert decision.budget_class == "zero-token"


def test_legal_synthesis_is_explicit_premium_but_never_authority():
    router = ContinuityRouter(runtime_state=ContinuityState.READY)
    decision = router.decide(RouteRequest("legal-synthesis", requires_synthesis=True))
    assert decision.route == "premium"
    assert decision.reason_code == "verified-context-synthesis"
    assert decision.authority_eligible is False


def test_routing_ledger_contains_metadata_only(tmp_path):
    path = tmp_path / ".continuity" / "routes.jsonl"
    ledger = RoutingLedger(path)
    request = RouteRequest("retrieval", requires_tools=True)
    decision = ContinuityRouter().decide(request)
    ledger.append(request_id="matter-secret-seed", request=request, decision=decision)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert set(payload) == {
        "request_id", "task_class", "route", "budget_class", "reason_code", "state"
    }
    assert payload["request_id"] != "matter-secret-seed"
    assert "prompt" not in payload
    assert "content" not in payload
    assert "matter" not in payload
