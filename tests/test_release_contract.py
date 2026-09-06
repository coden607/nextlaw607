import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_continuity_verification_metadata_declares_current_commands():
    path = ROOT / ".continuity" / "verification.json"
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert "tests" in payload["gates"]
    assert payload["commands"]["tests"] == "./scripts/verify-python.sh"
    assert payload["commands"]["typecheck"] == "./scripts/verify-web.sh"
    assert payload["performance_budgets"]["lcp_ms"] == 2500


def test_web_test_runner_is_node14_compatible():
    package = json.loads((ROOT / "apps" / "web" / "package.json").read_text(encoding="utf-8"))
    assert "node --test" not in package["scripts"]["test"]
    assert (ROOT / "apps" / "web" / "tests" / "run.mjs").is_file()


def test_verification_metadata_is_not_gitignored():
    import subprocess
    result = subprocess.run(
        ["git", "check-ignore", "-q", ".continuity/verification.json"],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode != 0


def test_every_declared_gate_has_a_command():
    payload = json.loads((ROOT / ".continuity" / "verification.json").read_text(encoding="utf-8"))
    missing = [gate for gate in payload["gates"] if gate not in payload["commands"]]
    assert missing == []


def test_release_verifier_enforces_browser_evidence_gate():
    core = (ROOT / "scripts" / "verify.sh").read_text(encoding="utf-8")
    release = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8")
    assert "browser-evidence-check.py" not in core
    assert "browser-evidence-check.py" in release
    assert (ROOT / "scripts" / "browser-evidence-check.py").is_file()


def test_browser_evidence_workflow_captures_before_release_verification():
    workflow = ROOT / ".github" / "workflows" / "browser-release-evidence.yml"
    assert workflow.is_file()
    text = workflow.read_text(encoding="utf-8")
    assert "browser-evidence.mjs" in text
    assert "verify-release.sh" in text
    assert text.index("browser-evidence.mjs") < text.index("verify-release.sh")
    assert "upload-artifact" in text
    assert "continue-on-error: true" in text
    assert "include-hidden-files: true" in text
