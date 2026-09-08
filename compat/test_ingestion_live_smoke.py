import asyncio

from nextlaw607.ingestion import CandidateSourceKind
from nextlaw607.ingestion.adapters import Crawl4AIAdapter, DoclingAdapter


LIVE_URL = "https://www.example.com"


def _assert_live_candidate(candidate, source_kind: CandidateSourceKind) -> None:
    assert candidate.source_kind is source_kind
    assert candidate.source_url == LIVE_URL
    assert candidate.trusted is False
    assert candidate.verified_authority is False
    assert len(candidate.content_sha256) == 64
    assert "Example Domain" in candidate.content


def test_docling_live_html_conversion_stays_untrusted():
    candidate = DoclingAdapter().convert(LIVE_URL)
    _assert_live_candidate(candidate, CandidateSourceKind.DOCLING)


def test_crawl4ai_live_crawl_stays_untrusted():
    candidate = asyncio.run(Crawl4AIAdapter().crawl(LIVE_URL))
    _assert_live_candidate(candidate, CandidateSourceKind.CRAWL4AI)
