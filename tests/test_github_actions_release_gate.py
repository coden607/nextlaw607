from pathlib import Path


WORKFLOWS = (
    Path('.github/workflows/ci.yml'),
    Path('.github/workflows/browser-release-evidence.yml'),
)
EXACT_REVISION = "${{ github.event.pull_request.head.sha || github.sha }}"


def test_release_workflows_use_read_only_permissions():
    for workflow in WORKFLOWS:
        text = workflow.read_text(encoding='utf-8')
        assert "permissions:\n  contents: read\n" in text, workflow


def test_every_checkout_uses_exact_feature_revision_without_persisted_credentials():
    for workflow in WORKFLOWS:
        lines = workflow.read_text(encoding='utf-8').splitlines()
        checkout_indexes = [
            index for index, line in enumerate(lines) if "uses: actions/checkout@v4" in line
        ]
        assert checkout_indexes, workflow
        for index in checkout_indexes:
            window = "\n".join(lines[index : index + 6])
            assert "with:" in window, (workflow, window)
            assert f"ref: {EXACT_REVISION}" in window, (workflow, window)
            assert "persist-credentials: false" in window, (workflow, window)


def test_release_artifacts_are_named_for_exact_revision():
    ci = Path('.github/workflows/ci.yml').read_text(encoding='utf-8')
    browser = Path('.github/workflows/browser-release-evidence.yml').read_text(encoding='utf-8')
    assert f"production-readiness-{EXACT_REVISION}" in ci
    assert f"nextlaw607-browser-evidence-{EXACT_REVISION}" in browser
