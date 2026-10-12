from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from hashlib import sha256
from urllib.parse import urlparse

from nextlaw607.authority import (
    CitationFirewall,
    LegalAuthority,
    VerificationDecision,
)

_MAX_CONTENT_CHARS = 2_000_000


class CandidateSourceKind(str, Enum):
    DOCLING = "docling"
    CRAWL4AI = "crawl4ai"


@dataclass(frozen=True)
class CandidateDocument:
    source_kind: CandidateSourceKind
    source_url: str
    content: str
    content_sha256: str
    trusted: bool = False
    verified_authority: bool = False


def ingest_candidate(
    *,
    source_kind: CandidateSourceKind,
    source_url: str,
    content: str,
) -> CandidateDocument:
    normalized_url = source_url.strip()
    parsed = urlparse(normalized_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("ingestion source URL must use https")
    if not content:
        raise ValueError("ingestion content is required")
    if len(content) > _MAX_CONTENT_CHARS:
        raise ValueError("ingestion content is too large")

    digest = sha256(content.encode("utf-8")).hexdigest()
    return CandidateDocument(
        source_kind=source_kind,
        source_url=normalized_url,
        content=content,
        content_sha256=digest,
    )


def verify_candidate_authority(
    candidate: CandidateDocument,
    authority: LegalAuthority,
    firewall: CitationFirewall,
    *,
    today: date | None = None,
) -> VerificationDecision:
    if candidate.source_url != authority.source_url:
        return VerificationDecision(
            False,
            "UNVERIFIED — DO NOT CITE",
            ("ingested candidate provenance does not match authority source",),
        )
    return firewall.verify(authority, today=today)
