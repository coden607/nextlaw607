from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Mapping


class ContinuityState(str, Enum):
    READY = "ready"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class RouteRequest:
    task_class: str
    requires_synthesis: bool = False
    requires_tools: bool = False
    sensitivity: str = "matter"


@dataclass(frozen=True)
class RouteDecision:
    route: str
    budget_class: str
    reason_code: str
    state: ContinuityState
    authority_eligible: bool = False


_BUDGETS: Mapping[str, str] = {
    "classification": "zero-token",
    "guardrail": "zero-token",
    "routing": "zero-token",
    "retrieval": "economical",
    "legal-synthesis": "premium",
}


def _task_class(value: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        raise ValueError("task_class is required")
    return normalized


class ContinuityRouter:
    """Privacy-safe Continuity/Jev routing boundary.

    Routing chooses execution cost/route only. It cannot verify or promote legal
    authority; CitationFirewall remains the sole legal trust boundary.
    """

    def __init__(
        self,
        *,
        jev_decide: Callable[[str], str] | None = None,
        runtime_state: ContinuityState = ContinuityState.DEGRADED,
    ) -> None:
        self._jev_decide = jev_decide
        self._runtime_state = runtime_state

    def decide(self, request: RouteRequest) -> RouteDecision:
        task = _task_class(request.task_class)
        budget = _BUDGETS.get(task, "economical")

        if task in {"classification", "guardrail", "routing"}:
            if self._jev_decide is not None and self._runtime_state is ContinuityState.READY:
                try:
                    route = str(self._jev_decide(task)).strip().lower()
                except Exception:
                    route = ""
                if route in {"deterministic", "local_free", "economical"}:
                    return RouteDecision(route, "zero-token", "jev", self._runtime_state)
            return RouteDecision("deterministic", "zero-token", "deterministic-fallback", self._runtime_state)

        if request.requires_synthesis or task == "legal-synthesis":
            return RouteDecision("premium", "premium", "verified-context-synthesis", self._runtime_state)

        if request.requires_tools:
            return RouteDecision("economical", budget, "tool-workflow", self._runtime_state)

        return RouteDecision("economical", budget, "default-economical", self._runtime_state)


class RoutingLedger:
    """Append-only metadata ledger that never accepts prompt or matter text."""

    _ALLOWED = {"task_class", "route", "budget_class", "reason_code", "state", "request_id"}

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    @staticmethod
    def opaque_request_id(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("request id seed is required")
        return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]

    def append(self, *, request_id: str, request: RouteRequest, decision: RouteDecision) -> None:
        payload = {
            "request_id": self.opaque_request_id(request_id),
            "task_class": _task_class(request.task_class),
            "route": decision.route,
            "budget_class": decision.budget_class,
            "reason_code": decision.reason_code,
            "state": decision.state.value,
        }
        if set(payload) != self._ALLOWED:
            raise RuntimeError("routing ledger schema violation")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
