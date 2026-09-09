from pathlib import Path


WORKFLOW = Path(".github/workflows/evaluation-live-smoke.yml")
SMOKE = Path("compat/test_evaluation_live_smoke.py")


def test_provider_backed_evaluation_workflow_is_controlled_and_revision_bound():
    assert WORKFLOW.exists(), "controlled Ragas/Claude live-evaluation workflow is required"
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
    assert "push:" not in text
    assert "secrets.ANTHROPIC_API_KEY" in text
    assert "NEXTLAW_EXACT_REVISION" in text
    assert "claude-sonnet-5" in text
    assert "persist-credentials: false" in text
    assert "evaluation-live-evidence.json" in text
    assert "actions/upload-artifact@v4" in text


def test_live_evaluation_smoke_uses_real_ragas_and_claude_without_authority_promotion():
    assert SMOKE.exists(), "provider-backed Ragas/Claude smoke is required"
    text = SMOKE.read_text(encoding="utf-8")

    assert "Anthropic" in text
    assert "llm_factory" in text
    assert "provider=\"anthropic\"" in text
    assert "Faithfulness" in text
    assert "ContextPrecision" in text
    assert "RagasAdapter" in text
    assert "ClaudeEvaluator" in text
    assert "combine_evaluation" in text
    assert "DETERMINISTIC_GATE_FAILED" in text
    assert "authority_eligible" in text
    assert "verified_context" in text
    assert "NEXTLAW_EXACT_REVISION" in text
