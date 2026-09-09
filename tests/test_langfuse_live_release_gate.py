from pathlib import Path


WORKFLOW = Path(".github/workflows/langfuse-live-export.yml")
SMOKE = Path("compat/test_langfuse_live_smoke.py")


def test_langfuse_live_export_workflow_is_controlled_and_revision_bound():
    assert WORKFLOW.exists(), "controlled Langfuse live-export workflow is required"
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
    assert "push:" not in text
    assert "secrets.LANGFUSE_PUBLIC_KEY" in text
    assert "secrets.LANGFUSE_SECRET_KEY" in text
    assert "LANGFUSE_BASE_URL" in text
    assert "github.sha" in text
    assert "persist-credentials: false" in text
    assert "langfuse-live-evidence.json" in text
    assert "actions/upload-artifact@v4" in text


def test_langfuse_live_smoke_uses_production_privacy_boundary_and_server_readback():
    assert SMOKE.exists(), "provider-backed Langfuse smoke is required"
    text = SMOKE.read_text(encoding="utf-8")

    assert "PrivacySafeTelemetry" in text
    assert "LangfuseSink" in text
    assert "create_trace_id" in text
    assert "start_as_current_observation" in text
    assert ".flush()" in text
    assert "api.observations.get_many" in text
    assert "authority_eligible" in text
    assert "[REDACTED]" in text
    assert "private client prompt" in text
    assert "client@example.com" in text
    assert "NEXTLAW_EXACT_REVISION" in text
