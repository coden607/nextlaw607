from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_is_non_root_and_does_not_bake_in_insecure_api_origin():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "USER nextlaw" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "NEXTLAW_API_ORIGIN=http://" not in dockerfile


def test_ci_has_real_docker_build_and_runtime_smoke_gate():
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "docker-runtime-smoke:" in workflow
    assert "docker build" in workflow
    assert "docker run" in workflow
    assert "docker inspect" in workflow
    assert "curl --fail" in workflow
