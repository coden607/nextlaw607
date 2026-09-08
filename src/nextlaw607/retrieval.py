from __future__ import annotations

import json
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EMBEDDING_DIMENSIONS = 1536
MAX_MATCH_COUNT = 20
MAX_CHUNK_CHARS = 200_000

RequestJson = Callable[[str, dict[str, str], dict[str, Any], float], tuple[int, Any]]


def _stdlib_request_json(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: float,
) -> tuple[int, Any]:
    request = Request(
        url,
        headers=headers,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(getattr(response, "status", response.getcode()))
            raw = response.read()
    except HTTPError as exc:
        status = int(exc.code)
        raw = exc.read()
    except (URLError, TimeoutError, OSError):
        return 0, None

    if not raw:
        return status, None
    try:
        return status, json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return status, None


@dataclass(frozen=True)
class RetrievedChunk:
    """A retrieval candidate, never legal authority by itself."""

    chunk_id: str
    source_url: str
    jurisdiction: str
    content: str
    content_sha256: str
    similarity: float
    trusted: bool = False
    verified_authority: bool = False
    authority_eligible: bool = False


class SupabasePgvectorRepository:
    """Server-only pgvector semantic retrieval with fail-closed parsing.

    Retrieval ranks candidate source text only. Results cannot self-promote to
    legal authority; any legal assertion must still be reconstructed as a
    LegalAuthority and pass CitationFirewall independently.
    """

    def __init__(
        self,
        project_url: str,
        secret_key: str,
        *,
        timeout: float = 8.0,
        request_json: RequestJson | None = None,
    ) -> None:
        normalized_url = project_url.strip().rstrip("/")
        normalized_key = secret_key.strip()
        if not normalized_url.startswith("https://"):
            raise ValueError("Supabase project URL must use https")
        if not normalized_key:
            raise ValueError("Supabase server secret key is required")
        if normalized_key.startswith("sb_publishable_"):
            raise ValueError("Supabase server secret key must not be a publishable key")
        if timeout <= 0:
            raise ValueError("Supabase pgvector timeout must be positive")

        self._project_url = normalized_url
        self._secret_key = normalized_key
        self._timeout = float(timeout)
        self._request_json = request_json or _stdlib_request_json

    def search(
        self,
        *,
        query_embedding: Sequence[float],
        jurisdiction: str,
        limit: int = 8,
    ) -> tuple[RetrievedChunk, ...]:
        embedding = self._validate_embedding(query_embedding)
        normalized_jurisdiction = jurisdiction.strip()
        if not normalized_jurisdiction or len(normalized_jurisdiction) > 64:
            raise ValueError("jurisdiction is required and must be at most 64 characters")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_MATCH_COUNT:
            raise ValueError(f"limit must be between 1 and {MAX_MATCH_COUNT}")

        url = f"{self._project_url}/rest/v1/rpc/match_legal_chunks"
        payload = {
            "query_embedding": embedding,
            "match_count": limit,
            "filter_jurisdiction": normalized_jurisdiction,
        }
        headers = {
            "apikey": self._secret_key,
            "Authorization": f"Bearer {self._secret_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            status, response = self._request_json(url, headers, payload, self._timeout)
        except Exception:
            return ()
        if status != 200 or not isinstance(response, list):
            return ()

        parsed: list[RetrievedChunk] = []
        for row in response:
            chunk = self._parse_row(row, normalized_jurisdiction)
            if chunk is None:
                return ()
            parsed.append(chunk)
        return tuple(parsed)

    @staticmethod
    def _validate_embedding(query_embedding: Sequence[float]) -> list[float]:
        if isinstance(query_embedding, (str, bytes)) or len(query_embedding) != EMBEDDING_DIMENSIONS:
            raise ValueError(f"query embedding must contain exactly {EMBEDDING_DIMENSIONS} values")
        values: list[float] = []
        for value in query_embedding:
            if isinstance(value, bool):
                raise ValueError("query embedding values must be finite numbers")
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("query embedding values must be finite numbers") from exc
            if not math.isfinite(number):
                raise ValueError("query embedding values must be finite numbers")
            values.append(number)
        return values

    @staticmethod
    def _parse_row(row: Any, jurisdiction: str) -> RetrievedChunk | None:
        if not isinstance(row, Mapping):
            return None
        chunk_id = row.get("id")
        source_url = row.get("source_url")
        row_jurisdiction = row.get("jurisdiction")
        content = row.get("content")
        content_sha256 = row.get("content_sha256")
        similarity = row.get("similarity")
        if not all(isinstance(value, str) and value for value in (
            chunk_id,
            source_url,
            row_jurisdiction,
            content,
            content_sha256,
        )):
            return None
        if not source_url.startswith("https://") or row_jurisdiction != jurisdiction:
            return None
        if len(content) > MAX_CHUNK_CHARS:
            return None
        if len(content_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in content_sha256):
            return None
        if isinstance(similarity, bool):
            return None
        try:
            similarity_value = float(similarity)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(similarity_value) or not -1.0 <= similarity_value <= 1.0:
            return None
        return RetrievedChunk(
            chunk_id=chunk_id,
            source_url=source_url,
            jurisdiction=row_jurisdiction,
            content=content,
            content_sha256=content_sha256.lower(),
            similarity=similarity_value,
        )
