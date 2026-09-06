from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

class AuthorityStatus(str, Enum):
    GOOD_LAW = "good_law"
    QUESTIONED = "questioned"
    OVERRULED = "overruled"
    SUPERSEDED = "superseded"
    UNKNOWN = "unknown"

class SourceTier(str, Enum):
    OFFICIAL = "official"
    REPOSITORY = "repository"
    SECONDARY = "secondary"

@dataclass(frozen=True)
class LegalAuthority:
    citation: str
    title: str
    court: str
    jurisdiction: str
    decision_date: date
    source_url: str
    source_tier: SourceTier
    holding: str
    status: AuthorityStatus = AuthorityStatus.UNKNOWN
    last_verified_on: date | None = None
    verification_sources: tuple[str, ...] = field(default_factory=tuple)
    citation_history_checked_on: date | None = None
    negative_treatment_found: bool | None = None
    history_sources: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class VerificationDecision:
    verified: bool
    label: str
    reasons: tuple[str, ...] = ()

class CitationFirewall:
    def __init__(self, max_age_days: int = 90) -> None:
        self.max_age_days = max_age_days

    def verify(self, authority: LegalAuthority, *, today: date | None = None) -> VerificationDecision:
        today = today or date.today()
        reasons: list[str] = []
        for name in ("citation", "title", "court", "jurisdiction", "holding", "source_url"):
            if not getattr(authority, name): reasons.append(f"missing {name}")
        if authority.status is not AuthorityStatus.GOOD_LAW: reasons.append("authority not confirmed good law")
        if authority.source_tier is SourceTier.SECONDARY: reasons.append("secondary source cannot verify authority")
        if not authority.verification_sources: reasons.append("no verification source")
        if authority.last_verified_on is None:
            reasons.append("never verified")
        elif (today - authority.last_verified_on).days > self.max_age_days:
            reasons.append("verification stale")
        if authority.citation_history_checked_on is None:
            reasons.append("citation history not reviewed")
        elif (today - authority.citation_history_checked_on).days > self.max_age_days:
            reasons.append("citation history review stale")
        if authority.negative_treatment_found is None:
            reasons.append("negative treatment not assessed")
        elif authority.negative_treatment_found:
            reasons.append("negative treatment found")
        if not authority.history_sources:
            reasons.append("no citation history source")
        if reasons:
            return VerificationDecision(False, "UNVERIFIED — DO NOT CITE", tuple(reasons))
        return VerificationDecision(True, "VERIFIED", ())
