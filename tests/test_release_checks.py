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
