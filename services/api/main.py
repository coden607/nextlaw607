from __future__ import annotations

import os
from datetime import datetime

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from nextlaw607.access import (
    FreeEntitlementProvider,
    IdentityVerificationError,
    resolve_access,
)
from nextlaw607.access_config import identity_provider_from_environment
from nextlaw607.encounter import EncounterMode
from nextlaw607.live import LiveEncounterEngine
from nextlaw607.procedure import CriminalCaseState, ProcedureStage

app = FastAPI(title="NextLaw607 API", version="0.2.0")
app.state.identity_provider = identity_provider_from_environment(os.environ)
app.state.entitlement_provider = FreeEntitlementProvider()
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


@app.get("/api/session")
def session(
    request: Request,
    authorization: str | None = Header(default=None),
) -> dict[str, object]:
    try:
        access = resolve_access(
            authorization,
            request.app.state.identity_provider,
            request.app.state.entitlement_provider,
        )
    except IdentityVerificationError as exc:
        raise HTTPException(status_code=401, detail="identity verification failed") from exc
    return access.as_dict()


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
