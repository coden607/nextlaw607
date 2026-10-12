from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pgvector_live_smoke_gate_is_wired_into_ci():
    smoke = ROOT / "compat" / "test_pgvector_live_smoke.py"
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert smoke.exists(), "controlled pgvector live-smoke test is missing"
    assert "pgvector-live-smoke:" in workflow
    assert "pytest -q compat/test_pgvector_live_smoke.py" in workflow
