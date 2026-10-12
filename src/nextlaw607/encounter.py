from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class EncounterMode(str, Enum):
    STREET_STOP = "street_stop"
    TRAFFIC_STOP = "traffic_stop"
    HOME_ENTRY = "home_entry"
    SEARCH = "search"
    INTERROGATION = "interrogation"
    ARREST = "arrest"

UNSAFE_TERMS = ("resist", "fight", "run", "flee", "hide evidence", "destroy evidence", "lie", "interfere", "obstruct")

@dataclass(frozen=True)
class EncounterSafetyDecision:
    allowed: bool
    guidance: tuple[str, ...]

class EncounterSafety:
    def evaluate_goal(self, goal: str) -> EncounterSafetyDecision:
        lowered = goal.lower()
        if any(term in lowered for term in UNSAFE_TERMS):
            return EncounterSafetyDecision(False, (
                "Do not resist, flee, interfere, lie, obstruct, or destroy evidence.",
                "Calmly state non-consent when appropriate and preserve the issue for later legal review.",
            ))
        return EncounterSafetyDecision(True, ())
