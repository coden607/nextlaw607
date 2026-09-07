from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from .sources import SourceCapability, SourceRegistry


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
            if not getattr(authority, name):
                reasons.append(f"missing {name}")
        if authority.status is not AuthorityStatus.GOOD_LAW:
            reasons.append("authority not confirmed good law")
        if authority.source_tier is SourceTier.SECONDARY:
            reasons.append("secondary source cannot verify authority")

        registry = SourceRegistry()
        official_text_verified = (
            registry.is_official_url(authority.source_url, authority.jurisdiction)
            and registry.supports(
                authority.source_url,
                SourceCapability.PRIMARY_TEXT,
                authority.jurisdiction,
            )
        )
        if not official_text_verified:
            official_text_verified = any(
                registry.is_official_url(source, authority.jurisdiction)
                and registry.supports(
                    source,
                    SourceCapability.PRIMARY_TEXT,
                    authority.jurisdiction,
                )
                for source in authority.verification_sources
            )
        if not official_text_verified:
            reasons.append("official source text not verified")
        if not authority.verification_sources:
            reasons.append("no verification source")
        elif not all(
            registry.supports(
                source,
                SourceCapability.PRIMARY_TEXT,
                authority.jurisdiction,
            )
            for source in authority.verification_sources
        ):
            reasons.append("verification source lacks primary-text capability")
        if authority.last_verified_on is None:
            reasons.append("never verified")
        elif authority.last_verified_on > today:
            reasons.append("verification date is in the future")
        elif authority.last_verified_on < authority.decision_date:
            reasons.append("verification predates decision")
        elif (today - authority.last_verified_on).days > self.max_age_days:
            reasons.append("verification stale")

        if authority.citation_history_checked_on is None:
            reasons.append("citation history not reviewed")
        elif authority.citation_history_checked_on > today:
            reasons.append("citation history review date is in the future")
        elif authority.citation_history_checked_on < authority.decision_date:
            reasons.append("citation history review predates decision")
        elif (
            authority.last_verified_on is not None
            and authority.citation_history_checked_on < authority.last_verified_on
        ):
            reasons.append("citation history review predates latest text verification")
        elif (today - authority.citation_history_checked_on).days > self.max_age_days:
            reasons.append("citation history review stale")
        if authority.negative_treatment_found is None:
            reasons.append("negative treatment not assessed")
        elif authority.negative_treatment_found:
            reasons.append("negative treatment found")
        if not authority.history_sources:
            reasons.append("no citation history source")
        elif not all(
            registry.supports(
                source,
                SourceCapability.CITATION_HISTORY,
                authority.jurisdiction,
            )
            for source in authority.history_sources
        ):
            reasons.append("citation history source lacks citation-history capability")
        elif len(authority.history_sources) > 1:
            provider_identities = tuple(
                registry.provider_identity(source, authority.jurisdiction)
                for source in authority.history_sources
            )
            if len(set(provider_identities)) != len(provider_identities):
                reasons.append("citation history sources are not independent")

        if reasons:
            return VerificationDecision(False, "UNVERIFIED — DO NOT CITE", tuple(reasons))
        return VerificationDecision(True, "VERIFIED", ())
