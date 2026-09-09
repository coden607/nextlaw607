from pathlib import Path


REQUIRED_GITHUB_SECRETS = {
    "MEM0_API_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "SENTRY_DSN",
    "SENTRY_AUTH_TOKEN",
    "SENTRY_ORG",
    "SENTRY_PROJECT",
    "ANTHROPIC_API_KEY",
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "NEXTLAW_API_ORIGIN",
    "CLOUDFLARE_DEPLOY_URL",
}

REQUIRED_GITHUB_VARIABLES = {
    "LANGFUSE_BASE_URL",
    "SENTRY_BASE_URL",
    "NEXTLAW_EVAL_MODEL",
}


def test_secret_bootstrap_contract_exists_and_is_fail_closed():
    manifest = Path("config/secrets.manifest")
    bootstrap = Path("scripts/setup-secrets.sh")

    assert manifest.exists(), "secret names manifest is required"
    assert bootstrap.exists(), "idempotent secret bootstrap script is required"

    manifest_text = manifest.read_text()
    bootstrap_text = bootstrap.read_text()

    for name in REQUIRED_GITHUB_SECRETS | REQUIRED_GITHUB_VARIABLES:
        assert name in manifest_text, f"missing declared environment name: {name}"

    assert "gh auth status" in bootstrap_text
    assert "gh secret set" in bootstrap_text
    assert "gh variable set" in bootstrap_text
    assert "wrangler secret put NEXTLAW_API_ORIGIN" in bootstrap_text
    assert "set -x" not in bootstrap_text
    assert "set +x" in bootstrap_text
    assert ".env" not in bootstrap_text
