from nextlaw607.ingestion import CandidateDocument, CandidateSourceKind, ingest_candidate


def test_docling_output_is_untrusted_candidate_with_hash_and_provenance():
    candidate = ingest_candidate(
        source_kind=CandidateSourceKind.DOCLING,
        source_url="https://example.com/opinion.pdf",
        content="People v Example\nSome extracted legal text.",
    )

    assert isinstance(candidate, CandidateDocument)
    assert candidate.trusted is False
    assert candidate.verified_authority is False
    assert candidate.source_kind is CandidateSourceKind.DOCLING
    assert candidate.source_url == "https://example.com/opinion.pdf"
    assert len(candidate.content_sha256) == 64


def test_crawl4ai_output_cannot_be_promoted_to_verified_authority():
    candidate = ingest_candidate(
        source_kind=CandidateSourceKind.CRAWL4AI,
        source_url="https://example.com/legal-summary",
        content="A secondary summary of a case.",
    )

    assert candidate.trusted is False
    assert candidate.verified_authority is False


def test_ingestion_rejects_unbounded_or_unsafe_inputs():
    try:
        ingest_candidate(
            source_kind=CandidateSourceKind.DOCLING,
            source_url="file:///tmp/private.pdf",
            content="x",
        )
    except ValueError as exc:
        assert "https" in str(exc).lower()
    else:
        raise AssertionError("non-HTTPS ingestion URL must fail closed")

    try:
        ingest_candidate(
            source_kind=CandidateSourceKind.DOCLING,
            source_url="https://example.com/too-large.pdf",
            content="x" * 2_000_001,
        )
    except ValueError as exc:
        assert "too large" in str(exc).lower()
    else:
        raise AssertionError("oversized ingestion content must fail closed")
