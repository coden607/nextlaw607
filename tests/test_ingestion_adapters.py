import asyncio

import pytest

from nextlaw607.ingestion import CandidateSourceKind
from nextlaw607.ingestion.adapters import Crawl4AIAdapter, DoclingAdapter


class _FakeDoclingDocument:
    def export_to_markdown(self):
        return "# People v Example\nVerified text candidate."


class _FakeDoclingResult:
    document = _FakeDoclingDocument()


class _FakeDoclingConverter:
    def convert(self, source):
        assert source == "https://example.com/opinion.pdf"
        return _FakeDoclingResult()


def test_docling_adapter_returns_untrusted_candidate_with_provenance():
    candidate = DoclingAdapter(converter=_FakeDoclingConverter()).convert(
        "https://example.com/opinion.pdf"
    )

    assert candidate.source_kind is CandidateSourceKind.DOCLING
    assert candidate.source_url == "https://example.com/opinion.pdf"
    assert candidate.content.startswith("# People v Example")
    assert candidate.trusted is False
    assert candidate.verified_authority is False


class _FakeCrawlResult:
    success = True
    markdown = "# Statute page\nUntrusted crawl output."


class _FakeCrawler:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def arun(self, *, url):
        assert url == "https://example.com/statute"
        return _FakeCrawlResult()


def test_crawl4ai_adapter_returns_untrusted_candidate_with_provenance():
    candidate = asyncio.run(
        Crawl4AIAdapter(crawler_factory=_FakeCrawler).crawl(
            "https://example.com/statute"
        )
    )

    assert candidate.source_kind is CandidateSourceKind.CRAWL4AI
    assert candidate.source_url == "https://example.com/statute"
    assert candidate.content.startswith("# Statute page")
    assert candidate.trusted is False
    assert candidate.verified_authority is False


def test_docling_adapter_fails_closed_on_empty_export():
    class EmptyDocument:
        def export_to_markdown(self):
            return ""

    class EmptyConverter:
        def convert(self, source):
            return type("Result", (), {"document": EmptyDocument()})()

    with pytest.raises(ValueError, match="content is required"):
        DoclingAdapter(converter=EmptyConverter()).convert(
            "https://example.com/empty.pdf"
        )


def test_crawl4ai_adapter_fails_closed_on_unsuccessful_result():
    class FailedCrawler(_FakeCrawler):
        async def arun(self, *, url):
            return type(
                "Result",
                (),
                {"success": False, "markdown": "partial", "error_message": "blocked"},
            )()

    with pytest.raises(RuntimeError, match="blocked"):
        asyncio.run(
            Crawl4AIAdapter(crawler_factory=FailedCrawler).crawl(
                "https://example.com/blocked"
            )
        )


def test_runtime_dependencies_fail_closed_when_missing(monkeypatch):
    import nextlaw607.ingestion.adapters as adapters

    monkeypatch.setattr(adapters, "_load_docling_converter", lambda: (_ for _ in ()).throw(RuntimeError("Docling runtime unavailable")))
    with pytest.raises(RuntimeError, match="Docling runtime unavailable"):
        DoclingAdapter()

    monkeypatch.setattr(adapters, "_load_crawl4ai_crawler", lambda: (_ for _ in ()).throw(RuntimeError("Crawl4AI runtime unavailable")))
    with pytest.raises(RuntimeError, match="Crawl4AI runtime unavailable"):
        Crawl4AIAdapter()
