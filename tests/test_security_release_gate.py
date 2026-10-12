from pathlib import Path


def test_security_workflow_is_exact_revision_fail_closed_gate():
    workflow = Path(".github/workflows/security.yml")
    assert workflow.exists(), "release security verification requires a dedicated workflow"

    text = workflow.read_text(encoding="utf-8")
    for required in (
        "permissions:",
        "contents: read",
        "actions/checkout@v4",
        "persist-credentials: false",
        "github.event.pull_request.head.sha || github.sha",
        "gitleaks/gitleaks-action@v2",
        "pip-audit --local",
        "npm audit --audit-level=high",
    ):
        assert required in text, required
