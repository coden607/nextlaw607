from pathlib import Path


def test_opentelemetry_requires_real_otlp_export_release_gate():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/opentelemetry-live-smoke.yml")
    smoke = Path("compat/test_opentelemetry_live_export.py")

    assert "opentelemetry-exporter-otlp-proto-http" in pyproject
    assert workflow.exists()
    assert smoke.exists()

    workflow_text = workflow.read_text(encoding="utf-8")
    smoke_text = smoke.read_text(encoding="utf-8")
    assert "compat/test_opentelemetry_live_export.py" in workflow_text
    assert "ExportTraceServiceRequest" in smoke_text
    assert "PrivacySafeTelemetry" in smoke_text
    assert "private client prompt" in smoke_text
    assert "client@example.com" in smoke_text
