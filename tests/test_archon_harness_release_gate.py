from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".archon/workflows/nextlaw-production.yaml")


def test_current_archon_harness_workflow_is_committed_and_fail_closed() -> None:
    assert WORKFLOW.is_file(), "current Archon harness workflow must be committed"

    text = WORKFLOW.read_text(encoding="utf-8")

    # Current (2026) Archon is a YAML workflow/harness engine above coding agents.
    assert "nodes:" in text
    assert "id: plan" in text
    assert "id: verify" in text
    assert "id: legal-trust-check" in text
    assert "id: review" in text

    # Deterministic release gates remain outside model discretion.
    assert "./scripts/verify.sh" in text
    assert "python3 scripts/production-readiness-check.py --require-ready" in text

    # Archon is development orchestration only; CitationFirewall remains authoritative.
    assert "development-only" in text
    assert "CitationFirewall" in text
    assert "never promote memory, model, retrieval, agent, tool, or orchestration output into legal evidence" in text

    # The harness must not contain credential material or secret interpolation.
    lowered = text.lower()
    assert "api_key:" not in lowered
    assert "secret_key:" not in lowered
    assert "authorization:" not in lowered
