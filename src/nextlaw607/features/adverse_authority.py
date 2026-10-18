from __future__ import annotations
_ADVERSE={"overruled","reversed","criticized","limited","distinguished","opposes"}

def identify(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    return [c for c in candidates if str(c.get("treatment","")).strip().lower() in _ADVERSE or str(c.get("posture","")).strip().lower()=="adverse"]

def research_complete(candidates: list[dict[str, object]], *, adverse_pass_ran: bool) -> bool:
    return bool(candidates) and adverse_pass_ran
