from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from nextlaw607.encounter import EncounterMode
from nextlaw607.live import LiveEncounterEngine
from nextlaw607.procedure import CriminalCaseState, ProcedureStage

_live = LiveEncounterEngine()


def dispatch(method: str, path: str, payload: Optional[Dict[str, Any]]) -> Tuple[int, Dict[str, Any]]:
    method = method.upper()
    if method == "GET" and path == "/status/live":
        return 200, {"status": "live"}
    if method == "GET" and path == "/status/ready":
        return 200, {"status": "ready"}
    if method == "POST" and path == "/api/live":
        data = payload or {}
        try:
            mode = EncounterMode(str(data.get("mode", "")))
        except ValueError:
            return 400, {"error": "invalid encounter mode"}
        response = _live.respond(mode, user_goal=str(data.get("user_goal") or "protect my rights"))
        return 200, {
            "say_now": list(response.say_now),
            "safety": list(response.safety),
            "preserve_for_later": list(response.preserve_for_later),
            "verified_authority": False,
            "authority_note": "Live safety guidance is not a substitute for current jurisdiction-specific authority verification.",
        }
    if method == "POST" and path == "/api/case/next-actions":
        data = payload or {}
        try:
            stage = ProcedureStage(str(data.get("stage") or ProcedureStage.INVESTIGATION.value))
        except ValueError:
            return 400, {"error": "invalid procedure stage"}
        next_appearance = data.get("next_appearance")
        parsed_appearance = None
        if next_appearance:
            try:
                parsed_appearance = datetime.fromisoformat(str(next_appearance))
            except ValueError:
                return 400, {"error": "invalid next_appearance"}
        state = CriminalCaseState(
            matter_id=str(data.get("matter_id") or "local"),
            jurisdiction=str(data.get("jurisdiction") or "NY"),
            stage=stage,
            next_appearance=parsed_appearance,
            unresolved_issues=list(data.get("unresolved_issues") or []),
        )
        return 200, {
            "stage": state.stage.value,
            "next_actions": list(state.next_actions()),
            "next_appearance": state.next_appearance.isoformat() if state.next_appearance else None,
            "deadline_source_verified": False,
        }
    return 404, {"error": "not found"}
