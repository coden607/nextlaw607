from __future__ import annotations
from dataclasses import dataclass
from .encounter import EncounterMode, EncounterSafety

@dataclass(frozen=True)
class LiveEncounterResponse:
    say_now: tuple[str, ...]
    safety: tuple[str, ...]
    preserve_for_later: tuple[str, ...]

class LiveEncounterEngine:
    def __init__(self) -> None:
        self.safety_engine = EncounterSafety()

    def respond(self, mode: EncounterMode, *, user_goal: str = "protect my rights") -> LiveEncounterResponse:
        safety = self.safety_engine.evaluate_goal(user_goal)
        if not safety.allowed:
            return LiveEncounterResponse((), safety.guidance, self._preserve())
        say = ["Stay calm. Do not physically resist or interfere."]
        if mode in {EncounterMode.SEARCH, EncounterMode.HOME_ENTRY, EncounterMode.TRAFFIC_STOP, EncounterMode.STREET_STOP}:
            say.append("I do not consent to any search.")
            say.append("Am I free to leave?")
        if mode is EncounterMode.INTERROGATION:
            say.extend(("I am invoking my right to remain silent.", "I want a lawyer before answering questions."))
        if mode is EncounterMode.ARREST:
            say.append("I want a lawyer and I am choosing to remain silent.")
        return LiveEncounterResponse(tuple(say), ("Follow lawful physical commands; preserve objections for court." ,), self._preserve())

    @staticmethod
    def _preserve() -> tuple[str, ...]:
        return ("Record time, location, agency, officer identifiers, witnesses, paperwork, and sequence of events when safe.",)
