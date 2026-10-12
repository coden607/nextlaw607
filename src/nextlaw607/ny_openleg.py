from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, Dict, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OPEN_LEG_BASE = "https://legislation.nysenate.gov/api/3"
Transport = Callable[[Request], Tuple[int, bytes]]


def _default_transport(request: Request) -> Tuple[int, bytes]:
    with urlopen(request, timeout=20) as response:  # nosec: HTTPS endpoint is fixed by default
        return response.status, response.read()


@dataclass(frozen=True)
class NYLawSection:
    law_id: str
    location_id: str
    title: str
    text: str
    active_date: Optional[date]
    repealed: bool
    source_url: str


class NYOpenLegClient:
    """Official NY Senate Open Legislation laws client with temporal snapshot support."""

    def __init__(self, api_key: str, *, transport: Optional[Transport] = None, base_url: str = OPEN_LEG_BASE) -> None:
        if not api_key:
            raise ValueError("Open Legislation API key is required")
        self.api_key = api_key
        self.transport = transport or _default_transport
        self.base_url = base_url.rstrip("/")

    def fetch_section(self, law_id: str, location_id: str, *, on_date: Optional[date] = None) -> NYLawSection:
        law_id = law_id.upper().strip()
        location_id = location_id.strip()
        if not law_id or not location_id:
            raise ValueError("law_id and location_id are required")

        if on_date is not None:
            params = {"date": on_date.isoformat(), "full": "true", "key": self.api_key}
            url = f"{self.base_url}/laws/{law_id}?{urlencode(params)}"
            payload = self._get(url)
            result = payload.get("result") or {}
            node = self._find_node(result.get("documents"), location_id)
            if node is None:
                raise LookupError(f"official NY law section not found: {law_id} {location_id}")
            provenance = f"{self.base_url}/laws/{law_id}?{urlencode({'date': on_date.isoformat(), 'full': 'true'})}"
            return self._section_from_node(law_id, location_id, node, provenance)

        url = f"{self.base_url}/laws/{law_id}/{location_id}?{urlencode({'key': self.api_key})}"
        payload = self._get(url)
        result = payload.get("result")
        if not isinstance(result, dict):
            raise LookupError(f"official NY law section not found: {law_id} {location_id}")
        provenance = f"{self.base_url}/laws/{law_id}/{location_id}"
        return self._section_from_node(law_id, location_id, result, provenance)

    def _get(self, url: str) -> Dict[str, Any]:
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "NextLaw607/0.2"}, method="GET")
        status, body = self.transport(request)
        if status != 200:
            raise RuntimeError(f"Open Legislation request failed with HTTP {status}")
        payload = json.loads(body)
        if not payload.get("success", False):
            raise RuntimeError("Open Legislation returned an unsuccessful response")
        return payload

    @classmethod
    def _find_node(cls, node: Any, location_id: str) -> Optional[Dict[str, Any]]:
        if not isinstance(node, dict):
            return None
        if str(node.get("locationId") or "") == location_id:
            return node
        children = ((node.get("documents") or {}).get("items") or []) if isinstance(node.get("documents"), dict) else []
        for child in children:
            found = cls._find_node(child, location_id)
            if found is not None:
                return found
        return None

    @staticmethod
    def _section_from_node(law_id: str, location_id: str, node: Dict[str, Any], source_url: str) -> NYLawSection:
        text = str(node.get("text") or "")
        if not text:
            raise LookupError(f"official NY law section has no text: {law_id} {location_id}")
        active = node.get("activeDate")
        return NYLawSection(
            law_id=law_id,
            location_id=location_id,
            title=str(node.get("title") or ""),
            text=text,
            active_date=date.fromisoformat(active) if active else None,
            repealed=bool(node.get("repealed", False)),
            source_url=source_url,
        )
