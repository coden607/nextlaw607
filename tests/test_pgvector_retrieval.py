import math

import pytest

from nextlaw607.retrieval import RetrievedChunk, SupabasePgvectorRepository


VALID_EMBEDDING = [0.01] * 1536


def _repo(request_json):
    return SupabasePgvectorRepository(
        "https://example.supabase.co",
        "sb_secret_server_only",
        request_json=request_json,
    )


def test_pgvector_search_returns_untrusted_candidates_with_provenance():
    captured = {}

    def request_json(url, headers, payload, timeout):
        captured.update(url=url, headers=headers, payload=payload, timeout=timeout)
        return 200, [
            {
                "id": "chunk-1",
                "source_url": "https://www.nycourts.gov/example",
                "jurisdiction": "NY",
                "content": "Extracted candidate legal text",
                "content_sha256": "a" * 64,
                "similarity": 0.91,
            }
        ]

    chunks = _repo(request_json).search(
        query_embedding=VALID_EMBEDDING,
        jurisdiction="NY",
        limit=5,
    )

    assert len(chunks) == 1
    chunk = chunks[0]
    assert isinstance(chunk, RetrievedChunk)
    assert chunk.source_url == "https://www.nycourts.gov/example"
    assert chunk.content_sha256 == "a" * 64
    assert chunk.trusted is False
    assert chunk.verified_authority is False
    assert chunk.authority_eligible is False
    assert captured["url"].endswith("/rest/v1/rpc/match_legal_chunks")
    assert captured["payload"]["filter_jurisdiction"] == "NY"
    assert captured["payload"]["match_count"] == 5
    assert captured["payload"]["query_embedding"] == VALID_EMBEDDING
    assert captured["headers"]["Authorization"].startswith("Bearer sb_secret_")


def test_pgvector_search_fails_closed_on_transport_status_or_shape_errors():
    cases = [
        lambda *_: (500, []),
        lambda *_: (200, {"not": "a list"}),
        lambda *_: (200, [{"id": "missing-fields"}]),
    ]

    for request_json in cases:
        assert _repo(request_json).search(
            query_embedding=VALID_EMBEDDING,
            jurisdiction="NY",
        ) == ()


def test_pgvector_search_rejects_unsafe_or_unbounded_inputs_before_network():
    calls = 0

    def request_json(*_):
        nonlocal calls
        calls += 1
        return 200, []

    repo = _repo(request_json)

    with pytest.raises(ValueError, match="1536"):
        repo.search(query_embedding=[0.1, 0.2], jurisdiction="NY")
    with pytest.raises(ValueError, match="finite"):
        repo.search(query_embedding=[math.nan] + [0.0] * 1535, jurisdiction="NY")
    with pytest.raises(ValueError, match="limit"):
        repo.search(query_embedding=VALID_EMBEDDING, jurisdiction="NY", limit=0)
    with pytest.raises(ValueError, match="jurisdiction"):
        repo.search(query_embedding=VALID_EMBEDDING, jurisdiction="")

    assert calls == 0


def test_pgvector_repository_requires_https_and_server_secret():
    with pytest.raises(ValueError, match="https"):
        SupabasePgvectorRepository("http://example.supabase.co", "sb_secret_x")
    with pytest.raises(ValueError, match="publishable"):
        SupabasePgvectorRepository("https://example.supabase.co", "sb_publishable_x")
