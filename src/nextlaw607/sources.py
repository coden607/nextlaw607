from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LegalSource:
    name: str
    jurisdiction: str
    official: bool
    base_url: str
    rank: int

class SourceRegistry:
    def __init__(self) -> None:
        self.sources = (
            LegalSource("New York State Unified Court System", "NY", True, "https://www.nycourts.gov", 100),
            LegalSource("New York Senate Open Legislation", "NY", True, "https://legislation.nysenate.gov", 95),
            LegalSource("New York Codes, Rules and Regulations", "NY", True, "https://govt.westlaw.com/nycrr", 90),
            LegalSource("Supreme Court of the United States", "US", True, "https://www.supremecourt.gov", 85),
            LegalSource("CourtListener", "US", False, "https://www.courtlistener.com", 80),
        )

    def ordered_for(self, jurisdiction: str) -> list[LegalSource]:
        return sorted(self.sources, key=lambda s: ((s.jurisdiction == jurisdiction), s.official, s.rank), reverse=True)
