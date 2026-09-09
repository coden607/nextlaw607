from pathlib import Path


WORKFLOW = Path(".github/workflows/evaluation-live-export.yml")
SMOKE = Path("compat/test_evaluation_live_smoke.py")


def test_evaluation_live_workflow_is_controlled_and_revision_bound():
    assert WORKFLOW.exists(), "controlled provider evaluation workflow is required"
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
    assert "push:" not in text
    assert "secrets.ANTHROPIC_API_KEY" in text
    assert "ANTHROPIC_EVAL_MODEL" in text
    assert "github.sha" in text
    assert "persist-credentials: false" in text
    assert "evaluation-live-evidence.json" in text
    assert "actions/upload-artifact@v4" in text


def test_evaluation_live_smoke_uses_ragas_and_independent_claude_gate():
    assert SMOKE.exists(), "provider-backed Ragas + Claude smoke is required"
    text = SMOKE.read_text(encoding="utf-8")

    assert "AsyncAnthropic" in text
    assert "llm_factory" in text
    assert "Faithfulness" in text
    assert "ContextPrecision" in text
    assert "ClaudeEvaluator" in text
    assert "combine_evaluation" in text
    assert "DeterministicEvalResult" in text
    assert "authority_eligible" in text
    assert "NEXTLAW_EXACT_REVISION" in text
    assert "evaluation-live-evidence.json" in text
