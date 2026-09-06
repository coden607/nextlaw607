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
