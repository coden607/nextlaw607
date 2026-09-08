from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_production_container_contract_exists_and_is_hardened() -> None:
    dockerfile = ROOT / "Dockerfile"
    dockerignore = ROOT / ".dockerignore"

    assert dockerfile.exists(), "production Dockerfile must exist"
    assert dockerignore.exists(), ".dockerignore must exist"

    text = dockerfile.read_text()
    assert "FROM node:22-alpine" in text
    assert "npm ci" in text
    assert "npm run build" in text
    assert "USER nextlaw" in text
    assert "ENV NODE_ENV=production" in text
    assert "HEALTHCHECK" in text
    assert 'CMD ["node", "server.mjs"]' in text

    ignored = dockerignore.read_text()
    for forbidden in (".git", ".env", "node_modules", "__pycache__", ".pytest_cache"):
        assert forbidden in ignored
