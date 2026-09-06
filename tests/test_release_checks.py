from pathlib import Path

from nextlaw607.release_checks import architecture_issues, secret_issues, pwa_issues


def test_secret_check_rejects_committed_api_key_value(tmp_path: Path):
    (tmp_path / "bad.txt").write_text("OPENAI_API_KEY=sk-live-secret\n", encoding="utf-8")
    issues = secret_issues(tmp_path, paths=[Path("bad.txt")])
    assert issues


def test_secret_check_allows_blank_example_value(tmp_path: Path):
    (tmp_path / ".env.example").write_text("OPENAI_API_KEY=\n", encoding="utf-8")
    assert secret_issues(tmp_path, paths=[Path(".env.example")]) == []


def test_architecture_check_requires_web_api_and_legal_core(tmp_path: Path):
    assert architecture_issues(tmp_path)
    for path in ["apps/web", "services/api", "src/nextlaw607", "tests"]:
        (tmp_path / path).mkdir(parents=True, exist_ok=True)
    assert architecture_issues(tmp_path) == []


def test_pwa_check_requires_manifest_service_worker_and_registration(tmp_path: Path):
    web = tmp_path / "apps" / "web"
    web.mkdir(parents=True)
    assert pwa_issues(tmp_path)
    (web / "manifest.webmanifest").write_text('{"name":"x","start_url":"/","display":"standalone","icons":[]}', encoding="utf-8")
    (web / "sw.js").write_text("self.addEventListener('fetch',()=>{})", encoding="utf-8")
    (web / "index.html").write_text('<link rel="manifest" href="/manifest.webmanifest"><script>navigator.serviceWorker.register("/sw.js")</script>', encoding="utf-8")
    assert pwa_issues(tmp_path) == []


def test_browser_evidence_fails_closed_when_missing(tmp_path: Path):
    from nextlaw607.release_checks import browser_evidence_issues
    metadata = {"performance_budgets": {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200}}
    issues = browser_evidence_issues(tmp_path, metadata=metadata, revision="abc123")
    assert "missing browser evidence" in issues


def test_browser_evidence_requires_exact_revision_and_all_browser_gates(tmp_path: Path):
    import json
    from nextlaw607.release_checks import browser_evidence_issues
    continuity = tmp_path / ".continuity"
    continuity.mkdir()
    (continuity / "browser-evidence.json").write_text(json.dumps({
        "revision": "wrong",
        "captured_at": "2026-09-06T20:00:00Z",
        "tool": "playwright+lighthouse",
        "e2e_passed": True,
        "accessibility_passed": True,
        "pwa_passed": True,
        "performance": {"lcp_ms": 1800, "cls": 0.03, "inp_ms": 120},
    }), encoding="utf-8")
    issues = browser_evidence_issues(
        tmp_path,
        metadata={"performance_budgets": {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200}},
        revision="abc123",
    )
    assert any("revision" in issue for issue in issues)


def test_browser_evidence_passes_when_provenance_and_budgets_match(tmp_path: Path):
    import json
    from nextlaw607.release_checks import browser_evidence_issues
    continuity = tmp_path / ".continuity"
    continuity.mkdir()
    (continuity / "browser-evidence.json").write_text(json.dumps({
        "revision": "abc123",
        "captured_at": "2026-09-06T20:00:00Z",
        "tool": "playwright+lighthouse",
        "e2e_passed": True,
        "accessibility_passed": True,
        "pwa_passed": True,
        "performance": {"lcp_ms": 1800, "cls": 0.03, "inp_ms": 120},
    }), encoding="utf-8")
    assert browser_evidence_issues(
        tmp_path,
        metadata={"performance_budgets": {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200}},
        revision="abc123",
    ) == []
