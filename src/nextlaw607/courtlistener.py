from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .authority import AuthorityStatus, LegalAuthority, SourceTier

COURTLISTENER_MCP_URL = "https://mcp.courtlistener.com/"
COURTLISTENER_API_BASE = "https://www.courtlistener.com/api/rest/v4"

Transport = Callable[[Request], tuple[int, bytes]]


def _default_transport(request: Request) -> tuple[int, bytes]:
    with urlopen(request, timeout=20) as response:  # nosec: fixed HTTPS endpoint by default
        return response.status, response.read()


@dataclass(frozen=True)
class CourtListenerSearchHit:
    cluster_id: int
    case_name: str
    citations: tuple[str, ...]
    court: str
    court_id: str
    date_filed: date | None
    absolute_url: str
    status: str

    @property
    def canonical_url(self) -> str:
        return f"https://www.courtlistener.com{self.absolute_url}"


class CourtListenerClient:
    """Small v4 REST client. Search results are candidates, never automatic good-law determinations."""

    def __init__(self, token: str | None = None, *, transport: Transport | None = None, base_url: str = COURTLISTENER_API_BASE) -> None:
        self.token = token
        self.transport = transport or _default_transport
        self.base_url = base_url.rstrip("/")

    def search_opinions(self, query: str, *, limit: int = 10) -> list[CourtListenerSearchHit]:
        params = urlencode({"q": query, "type": "o"})
        request = self._request(f"{self.base_url}/search/?{params}")
        status, body = self.transport(request)
        if status != 200:
            raise RuntimeError(f"CourtListener search failed with HTTP {status}")
        payload = json.loads(body)
        hits: list[CourtListenerSearchHit] = []
        for raw in payload.get("results", [])[:limit]:
            filed = date.fromisoformat(raw["dateFiled"]) if raw.get("dateFiled") else None
            hits.append(CourtListenerSearchHit(
                cluster_id=int(raw["cluster_id"]),
                case_name=str(raw.get("caseNameFull") or raw.get("caseName") or ""),
                citations=tuple(raw.get("citation") or ()),
                court=str(raw.get("court") or ""),
                court_id=str(raw.get("court_id") or ""),
                date_filed=filed,
                absolute_url=str(raw.get("absolute_url") or ""),
                status=str(raw.get("status") or ""),
            ))
        return hits

    def candidate_authority(self, hit: CourtListenerSearchHit, *, jurisdiction: str, holding: str = "") -> LegalAuthority:
        citation = hit.citations[0] if hit.citations else f"CourtListener cluster {hit.cluster_id}"
        return LegalAuthority(
            citation=citation,
            title=hit.case_name,
            court=hit.court,
            jurisdiction=jurisdiction,
            decision_date=hit.date_filed or date.min,
            source_url=hit.canonical_url,
            source_tier=SourceTier.REPOSITORY,
            holding=holding,
            status=AuthorityStatus.UNKNOWN,
            last_verified_on=None,
            verification_sources=(hit.canonical_url,),
        )

    def _request(self, url: str) -> Request:
        headers = {"Accept": "application/json", "User-Agent": "NextLaw607/0.2"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return Request(url, headers=headers, method="GET")
