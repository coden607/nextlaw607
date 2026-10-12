from pathlib import Path


WORKFLOW = Path(".github/workflows/sentry-live-export.yml")
SMOKE = Path("compat/test_sentry_live_smoke.py")


def test_sentry_live_export_workflow_is_controlled_and_revision_bound():
    assert WORKFLOW.exists(), "controlled Sentry live-export workflow is required"
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "pull_request:" not in text
    assert "push:" not in text
    assert "secrets.SENTRY_DSN" in text
    assert "secrets.SENTRY_AUTH_TOKEN" in text
    assert "secrets.SENTRY_ORG" in text
    assert "secrets.SENTRY_PROJECT" in text
    assert "github.sha" in text
    assert "persist-credentials: false" in text
    assert "sentry-live-evidence.json" in text
    assert "actions/upload-artifact@v4" in text


def test_sentry_live_smoke_uses_production_privacy_boundary_and_provider_readback():
    assert SMOKE.exists(), "provider-backed Sentry smoke is required"
    text = SMOKE.read_text(encoding="utf-8")

    assert "PrivacySafeTelemetry" in text
    assert "SentrySink" in text
    assert "sentry_sdk.init" in text
    assert "flush" in text
    assert "SENTRY_AUTH_TOKEN" in text
    assert "SENTRY_ORG" in text
    assert "SENTRY_PROJECT" in text
    assert "authority_eligible" in text
    assert "[REDACTED]" in text
    assert "private client prompt" in text
    assert "client@example.com" in text
    assert "NEXTLAW_EXACT_REVISION" in text
