from __future__ import annotations

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

from nextlaw607.encounter import EncounterMode
from nextlaw607.live import LiveEncounterEngine
from nextlaw607.procedure import CriminalCaseState, ProcedureStage

app = FastAPI(title="NextLaw607 API", version="0.2.0")
live_engine = LiveEncounterEngine()

class LiveRequest(BaseModel):
    mode: EncounterMode
    user_goal: str = "protect my rights"

class MatterRequest(BaseModel):
    matter_id: str
    jurisdiction: str = "NY"
    stage: ProcedureStage = ProcedureStage.INVESTIGATION
    next_appearance: datetime | None = None
    unresolved_issues: list[str] = Field(default_factory=list)

@app.get("/status/live")
def status_live() -> dict[str, str]:
    return {"status": "live"}

@app.get("/status/ready")
def status_ready() -> dict[str, str]:
    return {"status": "ready"}

@app.post("/api/live")
def live(request: LiveRequest) -> dict:
    response = live_engine.respond(request.mode, user_goal=request.user_goal)
    return {
        "say_now": list(response.say_now),
        "safety": list(response.safety),
        "preserve_for_later": list(response.preserve_for_later),
        "verified_authority": False,
        "authority_note": "Live safety guidance is not a substitute for current jurisdiction-specific authority verification.",
    }

@app.post("/api/case/next-actions")
def case_next_actions(request: MatterRequest) -> dict:
    state = CriminalCaseState(
        matter_id=request.matter_id,
        jurisdiction=request.jurisdiction,
        stage=request.stage,
        next_appearance=request.next_appearance,
        unresolved_issues=list(request.unresolved_issues),
    )
    return {
        "stage": state.stage.value,
        "next_actions": list(state.next_actions()),
        "next_appearance": state.next_appearance.isoformat() if state.next_appearance else None,
        "deadline_source_verified": False,
    }
