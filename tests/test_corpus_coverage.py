from datetime import date

import pytest

from nextlaw607.corpus_coverage import (
    CorpusCoverageObservation,
    CorpusCoverageTarget,
    CoverageState,
    coverage_summary,
    evaluate_corpus_coverage,
)


TARGET = CorpusCoverageTarget(
    source_id="ny-court-of-appeals",
    jurisdiction="NY",
    document_class="opinion",
    start_date=date(2020, 1, 1),
)


def test_complete_coverage_requires_dates_count_and_fresh_ingest():
    result = evaluate_corpus_coverage(
        TARGET,
        CorpusCoverageObservation(
            source_id="ny-court-of-appeals",
            jurisdiction="NY",
            document_class="opinion",
            earliest_date=date(2019, 1, 1),
            latest_date=date(2026, 10, 21),
            expected_documents=100,
            indexed_documents=100,
            last_successful_ingest=date(2026, 10, 20),
        ),
        today=date(2026, 10, 21),
    )
    assert result.state is CoverageState.COMPLETE
    assert result.coverage_ratio == 1.0
    assert result.reasons == ()


def test_partial_coverage_is_explicit_and_never_claimed_complete():
    result = evaluate_corpus_coverage(
        TARGET,
        CorpusCoverageObservation(
            source_id="ny-court-of-appeals",
            jurisdiction="NY",
            document_class="opinion",
            earliest_date=date(2021, 1, 1),
            latest_date=date(2026, 10, 1),
            expected_documents=100,
            indexed_documents=85,
            last_successful_ingest=date(2026, 9, 1),
        ),
        today=date(2026, 10, 21),
    )
    assert result.state is CoverageState.PARTIAL
    assert result.coverage_ratio == 0.85
    assert "indexed document count below expected count" in result.reasons
    assert "coverage does not reach target start date" in result.reasons
    assert "ingestion freshness is stale" in result.reasons


def test_missing_observation_fails_closed():
    result = evaluate_corpus_coverage(TARGET, None, today=date(2026, 10, 21))
    assert result.state is CoverageState.MISSING
    assert result.coverage_ratio == 0.0


def test_identity_mismatch_is_unknown_not_complete():
    result = evaluate_corpus_coverage(
        TARGET,
        CorpusCoverageObservation(
            source_id="other-source",
            jurisdiction="NY",
            document_class="opinion",
            earliest_date=date(2019, 1, 1),
            latest_date=date(2026, 10, 21),
            expected_documents=100,
            indexed_documents=100,
            last_successful_ingest=date(2026, 10, 21),
        ),
        today=date(2026, 10, 21),
    )
    assert result.state is CoverageState.UNKNOWN
    assert result.coverage_ratio is None


def test_summary_and_input_validation():
    missing = evaluate_corpus_coverage(TARGET, None, today=date(2026, 10, 21))
    assert coverage_summary([missing]) == {
        "complete": 0,
        "partial": 0,
        "missing": 1,
        "unknown": 0,
    }
    with pytest.raises(ValueError, match="end_date"):
        CorpusCoverageTarget(
            source_id="x",
            jurisdiction="NY",
            document_class="opinion",
            start_date=date(2026, 1, 2),
            end_date=date(2026, 1, 1),
        )
    with pytest.raises(ValueError, match="stale_after_days"):
        evaluate_corpus_coverage(TARGET, None, today=date(2026, 10, 21), stale_after_days=-1)
