from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ingestion_live_smoke_gate_is_wired_into_ci():
    smoke = ROOT / "compat" / "test_ingestion_live_smoke.py"
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert smoke.exists(), "controlled ingestion live-smoke test is missing"
    assert "ingestion-live-smoke:" in workflow
    assert "pytest -q compat/test_ingestion_live_smoke.py" in workflow
    assert "playwright install --with-deps chromium" in workflow
