from __future__ import annotations

from collections.abc import Callable
from typing import Any

from nextlaw607.ingestion import CandidateDocument, CandidateSourceKind, ingest_candidate


def _load_docling_converter() -> Any:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise RuntimeError(
            "Docling runtime unavailable; install nextlaw607-core[ingestion]"
        ) from exc
    return DocumentConverter()


def _load_crawl4ai_crawler() -> Callable[[], Any]:
    try:
        from crawl4ai import AsyncWebCrawler
    except ImportError as exc:
        raise RuntimeError(
            "Crawl4AI runtime unavailable; install nextlaw607-core[ingestion]"
        ) from exc
    return AsyncWebCrawler


def _markdown_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    raw_markdown = getattr(value, "raw_markdown", None)
    if isinstance(raw_markdown, str):
        return raw_markdown
    return ""


class DoclingAdapter:
    """Convert a document into an untrusted ingestion candidate.

    Docling extraction is a parsing convenience only. Its output cannot become
    legal authority without the deterministic CitationFirewall path.
    """

    def __init__(self, *, converter: Any | None = None) -> None:
        self._converter = converter if converter is not None else _load_docling_converter()

    def convert(self, source_url: str) -> CandidateDocument:
        try:
            result = self._converter.convert(source_url)
            document = result.document
            content = document.export_to_markdown()
        except Exception as exc:
            if isinstance(exc, (ValueError, RuntimeError)):
                raise
            raise RuntimeError("Docling conversion failed") from exc

        return ingest_candidate(
            source_kind=CandidateSourceKind.DOCLING,
            source_url=source_url,
            content=content,
        )


class Crawl4AIAdapter:
    """Crawl a web page into an untrusted ingestion candidate."""

    def __init__(self, *, crawler_factory: Callable[[], Any] | None = None) -> None:
        self._crawler_factory = (
            crawler_factory if crawler_factory is not None else _load_crawl4ai_crawler()
        )

    async def crawl(self, source_url: str) -> CandidateDocument:
        try:
            async with self._crawler_factory() as crawler:
                result = await crawler.arun(url=source_url)
        except Exception as exc:
            raise RuntimeError("Crawl4AI crawl failed") from exc

        if getattr(result, "success", True) is False:
            error = getattr(result, "error_message", None)
            detail = str(error).strip() if error else "crawl unsuccessful"
            raise RuntimeError(f"Crawl4AI crawl failed: {detail}")

        content = _markdown_text(getattr(result, "markdown", ""))
        return ingest_candidate(
            source_kind=CandidateSourceKind.CRAWL4AI,
            source_url=source_url,
            content=content,
        )
