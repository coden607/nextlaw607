from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ProcedureStage(str, Enum):
    INVESTIGATION = "investigation"
    ARREST = "arrest"
    APPEARANCE_TICKET = "appearance_ticket"
    ARRAIGNMENT = "arraignment"
    RELEASE_BAIL_REMAND = "release_bail_remand"
    GRAND_JURY = "grand_jury"
    PLEA = "plea"
    PRETRIAL = "pretrial"
    DISCOVERY = "discovery"
    MOTIONS = "motions"
    HEARINGS = "hearings"
    TRIAL = "trial"
    SENTENCING = "sentencing"
    APPEAL = "appeal"
    POST_CONVICTION = "post_conviction"

@dataclass(frozen=True)
class CaseEvent:
    stage: ProcedureStage
    occurred_at: datetime
    title: str
    source: str | None = None
    notes: str | None = None

@dataclass
class CriminalCaseState:
    matter_id: str
    jurisdiction: str
    stage: ProcedureStage = ProcedureStage.INVESTIGATION
    events: list[CaseEvent] = field(default_factory=list)
    unresolved_issues: list[str] = field(default_factory=list)
    next_appearance: datetime | None = None

    def record(self, event: CaseEvent) -> None:
        if self.events and event.occurred_at < self.events[-1].occurred_at:
            raise ValueError("events must be recorded in chronological order")
        self.events.append(event)
        self.stage = event.stage

    def next_actions(self) -> tuple[str, ...]:
        common = ("Preserve all court papers, release conditions, discovery, and attorney communications you choose to store.",)
        stage_actions = {
            ProcedureStage.INVESTIGATION: ("Avoid discussing case facts with investigators before obtaining legal advice.",),
            ProcedureStage.ARREST: ("Ask for counsel and preserve arrest/release paperwork.",),
            ProcedureStage.APPEARANCE_TICKET: ("Confirm the court, date, time, and appearance instructions shown on the ticket.",),
            ProcedureStage.ARRAIGNMENT: ("Confirm counsel, charges, release/bail conditions, and the next court date.",),
            ProcedureStage.RELEASE_BAIL_REMAND: ("Confirm release, bail, remand, supervision conditions, and the next appearance from the court paperwork.",),
            ProcedureStage.GRAND_JURY: ("Track grand jury status and preserve notices, counsel guidance, and related paperwork without assuming an outcome.",),
            ProcedureStage.PLEA: ("Review any plea terms, consequences, waivers, and sentencing exposure with counsel before deciding.",),
            ProcedureStage.PRETRIAL: ("Track appearances, discovery status, conditions, and unresolved legal issues.",),
            ProcedureStage.DISCOVERY: ("Inventory what was received and flag missing or unclear items for counsel review.",),
            ProcedureStage.MOTIONS: ("Track motion issues, filing status, responses, and hearing dates.",),
            ProcedureStage.HEARINGS: ("Prepare the factual timeline and verified legal issues with counsel.",),
            ProcedureStage.TRIAL: ("Track trial dates, evidence issues, witnesses, and preserved objections with counsel.",),
            ProcedureStage.SENTENCING: ("Confirm sentencing materials, conditions, and collateral-consequence questions for counsel.",),
            ProcedureStage.APPEAL: ("Preserve notices, deadlines, transcripts, orders, and issues identified by appellate counsel.",),
            ProcedureStage.POST_CONVICTION: ("Organize the record, prior rulings, newly discovered evidence, and counsel-reviewed grounds.",),
        }
        return stage_actions[self.stage] + common
