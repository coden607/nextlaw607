from pathlib import Path


def test_live_provider_workflows_exist_and_use_protected_secrets():
    expected = {
        ".github/workflows/langfuse-live-smoke.yml": ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"),
        ".github/workflows/sentry-live-smoke.yml": ("SENTRY_DSN",),
        ".github/workflows/evaluation-live-smoke.yml": ("ANTHROPIC_API_KEY",),
    }

    for workflow_path, secret_names in expected.items():
        text = Path(workflow_path).read_text(encoding="utf-8")
        assert "workflow_dispatch:" in text or "pull_request:" in text
        assert "permissions:" in text
        for secret_name in secret_names:
            assert f"secrets.{secret_name}" in text
        assert "continue-on-error: true" not in text
        assert "live smoke" in text.lower()


def test_live_provider_workflows_do_not_leak_secret_values_to_shell_output():
    for workflow_path in (
        ".github/workflows/langfuse-live-smoke.yml",
        ".github/workflows/sentry-live-smoke.yml",
        ".github/workflows/evaluation-live-smoke.yml",
    ):
        text = Path(workflow_path).read_text(encoding="utf-8")
        assert "set -x" not in text
        assert "echo $" not in text
        assert "printenv" not in text
