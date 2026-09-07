from __future__ import annotations
from dataclasses import dataclass
from .authority import CitationFirewall, LegalAuthority, VerificationDecision

@dataclass(frozen=True)
class LegalResearchRequest:
    question: str
    jurisdiction: str
    as_of_date: str | None = None

@dataclass(frozen=True)
class VerifiedAuthority:
    authority: LegalAuthority
    verification: VerificationDecision

@dataclass(frozen=True)
class LegalResearchResult:
    request: LegalResearchRequest
    authorities: tuple[VerifiedAuthority, ...]

    @property
    def citable_authorities(self) -> tuple[VerifiedAuthority, ...]:
        return tuple(a for a in self.authorities if a.verification.verified)

class ResearchWorkflow:
    def __init__(self, firewall: CitationFirewall | None = None) -> None:
        self.firewall = firewall or CitationFirewall()

    def evaluate(self, request: LegalResearchRequest, authorities: list[LegalAuthority]) -> LegalResearchResult:
        verified = tuple(VerifiedAuthority(a, self.firewall.verify(a)) for a in authorities)
        return LegalResearchResult(request, verified)
