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
    source_kind: str | None = None


@dataclass(frozen=True)
class CaseDeadline:
    title: str
    due_at: datetime
    source: str
    source_kind: str


@dataclass
class CriminalCaseState:
    matter_id: str
    jurisdiction: str
    stage: ProcedureStage = ProcedureStage.INVESTIGATION
    events: list[CaseEvent] = field(default_factory=list)
    unresolved_issues: list[str] = field(default_factory=list)
    deadlines: list[CaseDeadline] = field(default_factory=list)
    next_appearance: datetime | None = None
    next_appearance_source: str | None = None
    next_appearance_source_kind: str | None = None

    def record(self, event: CaseEvent, *, as_of: datetime | None = None) -> None:
        if as_of is not None and event.occurred_at > as_of:
            raise ValueError("event timestamp is in the future")
        trusted_source_kinds = {
            "court_notice",
            "docket",
            "counsel_confirmation",
            "police_record",
            "filed_document",
        }
        has_source = event.source is not None and bool(event.source.strip())
        if has_source and event.source_kind not in trusted_source_kinds:
            raise ValueError("event source requires a trusted source kind")
        if event.source_kind is not None and not has_source:
            raise ValueError("event source kind requires a source")
        if self.events and event.occurred_at < self.events[-1].occurred_at:
            raise ValueError("events must be recorded in chronological order")
        self.events.append(event)
        self.stage = event.stage

    def set_next_appearance(self, when: datetime, *, source: str, source_kind: str | None = None) -> None:
        if not source.strip():
            raise ValueError("next appearance requires a source")
        trusted_kinds = {"court_notice", "docket", "counsel_confirmation"}
        if source_kind not in trusted_kinds:
            raise ValueError("next appearance requires a trusted source kind")
        self.next_appearance = when
        self.next_appearance_source = source.strip()
        self.next_appearance_source_kind = source_kind

    def add_deadline(self, title: str, due_at: datetime, *, source: str, source_kind: str) -> None:
        if not title.strip():
            raise ValueError("deadline requires a title")
        if not source.strip():
            raise ValueError("deadline requires a source")
        trusted_kinds = {
            "court_notice",
            "docket",
            "counsel_confirmation",
            "statute",
            "court_rule",
        }
        if source_kind not in trusted_kinds:
            raise ValueError("deadline requires a trusted source kind")
        self.deadlines.append(
            CaseDeadline(
                title=title.strip(),
                due_at=due_at,
                source=source.strip(),
                source_kind=source_kind,
            )
        )
        self.deadlines.sort(key=lambda deadline: deadline.due_at)

    def next_actions(self, *, as_of: datetime | None = None) -> tuple[str, ...]:
        common = (
            "Preserve all court papers, release conditions, discovery, and attorney communications you choose to store.",
        )
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
        appearance: tuple[str, ...] = ()
        if self.next_appearance is not None:
            if self.next_appearance_source and self.next_appearance_source_kind:
                if as_of is not None and self.next_appearance < as_of:
                    appearance = (
                        f"Past-dated verified appearance: {self.next_appearance.isoformat()} — source: {self.next_appearance_source}. Re-check current court or counsel source before relying on this date.",
                    )
                else:
                    appearance = (
                        f"Verified next appearance: {self.next_appearance.isoformat()} — source: {self.next_appearance_source}.",
                    )
            else:
                appearance = (
                    "An unverified next-appearance date is stored; confirm it against court or counsel paperwork before relying on it.",
                )

        deadline_actions: list[str] = []
        for deadline in self.deadlines:
            label = "Source-backed deadline"
            if as_of is not None:
                label = "OVERDUE source-backed deadline" if deadline.due_at < as_of else "Upcoming source-backed deadline"
            deadline_actions.append(
                f"{label}: {deadline.title}: {deadline.due_at.isoformat()} — source: {deadline.source}."
            )
        return stage_actions[self.stage] + appearance + tuple(deadline_actions) + common
