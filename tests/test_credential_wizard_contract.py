from pathlib import Path


REQUIRED_PROVIDERS = {
    "supabase",
    "mem0",
    "langfuse",
    "sentry",
    "anthropic",
    "cloudflare",
}


def test_interactive_credential_wizard_contract():
    wizard = Path("scripts/credential-wizard.sh")
    routes = Path("config/provider-credential-urls.tsv")

    assert wizard.exists(), "interactive credential wizard is required"
    assert routes.exists(), "provider onboarding URL inventory is required"

    wizard_text = wizard.read_text(encoding="utf-8")
    routes_text = routes.read_text(encoding="utf-8")

    for provider in REQUIRED_PROVIDERS:
        assert provider in routes_text.lower(), f"missing provider route: {provider}"

    assert "https://" in routes_text
    assert "open_url" in wizard_text
    assert "read_clipboard" in wizard_text
    assert "gh secret set" in wizard_text
    assert "gh variable set" in wizard_text
    assert "wrangler secret put" in wizard_text
    assert "--status" in wizard_text
    assert "--no-open" in wizard_text
    assert "--provider" in wizard_text
    assert "set +x" in wizard_text
    assert "set -x" not in wizard_text
    assert ".env" not in wizard_text
    assert "password" not in wizard_text.lower()
    assert "mfa" not in wizard_text.lower()
