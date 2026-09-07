from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse


class SourceCapability(str, Enum):
    PRIMARY_TEXT = "primary_text"
    CITATION_HISTORY = "citation_history"
    PROCEDURE = "procedure"
    DOCKET = "docket"


@dataclass(frozen=True)
class LegalSource:
    name: str
    jurisdiction: str
    official: bool
    base_url: str
    rank: int
    capabilities: frozenset[SourceCapability] = frozenset()


class SourceRegistry:
    def __init__(self) -> None:
        primary = SourceCapability.PRIMARY_TEXT
        history = SourceCapability.CITATION_HISTORY
        procedure = SourceCapability.PROCEDURE
        docket = SourceCapability.DOCKET
        self.sources = (
            LegalSource(
                "New York State Unified Court System",
                "NY",
                True,
                "https://www.nycourts.gov",
                100,
                frozenset({primary, history, procedure}),
            ),
            LegalSource(
                "New York Senate Open Legislation",
                "NY",
                True,
                "https://legislation.nysenate.gov",
                95,
                frozenset({primary}),
            ),
            LegalSource(
                "New York Department of State",
                "NY",
                True,
                "https://dos.ny.gov",
                93,
                frozenset({primary, procedure}),
            ),
            LegalSource(
                "New York Codes, Rules and Regulations public viewer",
                "NY",
                False,
                "https://govt.westlaw.com/nycrr",
                90,
                frozenset({primary}),
            ),
            LegalSource(
                "Supreme Court of the United States",
                "US",
                True,
                "https://www.supremecourt.gov",
                88,
                frozenset({primary, history, procedure}),
            ),
            LegalSource(
                "United States Court of Appeals for the Second Circuit",
                "US",
                True,
                "https://www.ca2.uscourts.gov",
                87,
                frozenset({primary, history, procedure}),
            ),
            LegalSource(
                "Northern District of New York",
                "US",
                True,
                "https://www.nynd.uscourts.gov",
                86,
                frozenset({primary, procedure, docket}),
            ),
            LegalSource(
                "United States Code",
                "US",
                True,
                "https://uscode.house.gov",
                85,
                frozenset({primary}),
            ),
            LegalSource(
                "GovInfo",
                "US",
                True,
                "https://www.govinfo.gov",
                84,
                frozenset({primary}),
            ),
            LegalSource(
                "CourtListener",
                "ALL",
                False,
                "https://www.courtlistener.com",
                80,
                frozenset({history}),
            ),
            LegalSource(
                "CourtListener",
                "ALL",
                False,
                "https://api.courtlistener.com",
                80,
                frozenset({history}),
            ),
        )

    def ordered_for(self, jurisdiction: str) -> list[LegalSource]:
        return sorted(
            self.sources,
            key=lambda s: ((s.jurisdiction == jurisdiction), s.official, s.rank),
            reverse=True,
        )

    @staticmethod
    def _host_matches(url: str, base_url: str) -> bool:
        parsed = urlparse(url)
        source_parsed = urlparse(base_url)
        if parsed.scheme.lower() != "https" or source_parsed.scheme.lower() != "https":
            return False
        host = (parsed.hostname or "").lower()
        source_host = (source_parsed.hostname or "").lower()
        if not host or not source_host:
            return False
        root = source_host[4:] if source_host.startswith("www.") else source_host
        candidate_root = host[4:] if host.startswith("www.") else host
        if candidate_root != root:
            return False

        source_path = source_parsed.path.rstrip("/")
        if not source_path:
            return True
        candidate_path = parsed.path.rstrip("/")
        return candidate_path == source_path or candidate_path.startswith(source_path + "/")

    @staticmethod
    def _applies_to(source: LegalSource, jurisdiction: str | None) -> bool:
        if jurisdiction is None:
            return True
        applicable = {jurisdiction, "ALL"}
        if jurisdiction == "NY":
            applicable.add("US")
        return source.jurisdiction in applicable

    def provider_identity(self, url: str, jurisdiction: str | None = None) -> str | None:
        matches = [
            source
            for source in self.sources
            if self._applies_to(source, jurisdiction)
            and self._host_matches(url, source.base_url)
        ]
        if not matches:
            return None
        return max(matches, key=lambda source: source.rank).name

    def is_official_url(self, url: str, jurisdiction: str | None = None) -> bool:
        return any(
            source.official
            and self._applies_to(source, jurisdiction)
            and self._host_matches(url, source.base_url)
            for source in self.sources
        )

    def is_registered_url(self, url: str) -> bool:
        return any(self._host_matches(url, source.base_url) for source in self.sources)

    def supports(
        self,
        url: str,
        capability: SourceCapability | str,
        jurisdiction: str | None = None,
    ) -> bool:
        try:
            requested = capability if isinstance(capability, SourceCapability) else SourceCapability(capability)
        except ValueError:
            return False
        return any(
            self._applies_to(source, jurisdiction)
            and self._host_matches(url, source.base_url)
            and requested in source.capabilities
            for source in self.sources
        )
