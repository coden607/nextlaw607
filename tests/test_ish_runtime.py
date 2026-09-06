import json
from pathlib import Path

from services.api.fallback import dispatch

ROOT = Path(__file__).resolve().parents[1]


def test_project_declares_python39_floor_for_ish():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires-python = ">=3.9"' in text


def test_web_build_targets_node14_compatible_ecmascript():
    config = json.loads((ROOT / "apps" / "web" / "tsconfig.json").read_text(encoding="utf-8"))
    assert config["compilerOptions"]["target"] in {"ES2019", "ES2020"}


def test_fallback_api_matches_health_and_live_contract():
    status, body = dispatch("GET", "/status/live", None)
    assert status == 200
    assert body == {"status": "live"}

    status, body = dispatch("POST", "/api/live", {"mode": "search", "user_goal": "protect my rights"})
    assert status == 200
    assert "say_now" in body
    assert body["verified_authority"] is False


def test_dev_launcher_has_standard_library_api_fallback():
    text = (ROOT / "scripts" / "dev.sh").read_text(encoding="utf-8")
    assert "api_fallback.py" in text
