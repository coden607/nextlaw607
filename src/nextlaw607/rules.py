from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum

class RuleSourceKind(str, Enum):
    OFFICIAL = "official"
    VERIFIED_CASE = "verified_case"

@dataclass(frozen=True)
class LegalRule:
    id: str
    jurisdiction: str
    topic: str
    statement: str
    source_url: str
    source_kind: RuleSourceKind
    verified_on: date
    effective_from: date | None = None
    effective_to: date | None = None
    authority_ids: tuple[str, ...] = ()

    def effective_on(self, when: date) -> bool:
        if self.effective_from and when < self.effective_from:
            return False
        if self.effective_to and when > self.effective_to:
            return False
        return True

    def fresh_on(self, today: date, max_age_days: int) -> bool:
        age=(today-self.verified_on).days
        return 0 <= age <= max_age_days

class RuleRegistry:
    def __init__(self, rules: list[LegalRule] | None = None, *, max_verification_age_days: int = 90) -> None:
        self.rules=list(rules or [])
        self.max_verification_age_days=max_verification_age_days

    def add(self, rule: LegalRule) -> None:
        if any(existing.id == rule.id for existing in self.rules):
            raise ValueError(f"duplicate rule id: {rule.id}")
        self.rules.append(rule)

    def applicable(self, *, topic: str, jurisdiction: str, on_date: date, today: date | None = None) -> tuple[LegalRule, ...]:
        today=today or date.today()
        return tuple(rule for rule in self.rules if
            rule.topic == topic and
            rule.jurisdiction == jurisdiction and
            rule.effective_on(on_date) and
            rule.fresh_on(today, self.max_verification_age_days) and
            bool(rule.source_url) and
            bool(rule.statement)
        )

    def require(self, *, topic: str, jurisdiction: str, on_date: date, today: date | None = None) -> tuple[LegalRule, ...]:
        matches=self.applicable(topic=topic,jurisdiction=jurisdiction,on_date=on_date,today=today)
        if not matches:
            raise LookupError("no fresh verified rule for jurisdiction/date/topic")
        return matches
