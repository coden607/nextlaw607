from crawl4ai import AsyncWebCrawler
from docling.document_converter import DocumentConverter

from nextlaw607.ingestion.adapters import (
    _load_crawl4ai_crawler,
    _load_docling_converter,
)


def test_installed_docling_runtime_matches_adapter_contract():
    converter = _load_docling_converter()
    assert isinstance(converter, DocumentConverter)
    assert callable(converter.convert)


def test_installed_crawl4ai_runtime_matches_adapter_contract():
    crawler_factory = _load_crawl4ai_crawler()
    assert crawler_factory is AsyncWebCrawler
    assert callable(getattr(AsyncWebCrawler, "arun", None))
