from nextlaw607.guardrails import ToolAuthorizer


def test_tool_authorization_defaults_to_deny():
    auth = ToolAuthorizer()
    denied = auth.authorize("official_source_fetch")
    assert denied.allowed is False
    assert "allowlist" in denied.reason.lower()


def test_tool_authorization_requires_exact_explicit_allowlist_match():
    auth = ToolAuthorizer(allowed_tools={"official_source_fetch"})
    assert auth.authorize("official_source_fetch").allowed is True
    assert auth.authorize("Official_Source_Fetch").allowed is False
    assert auth.authorize(" official_source_fetch ").allowed is False


def test_tool_authorization_rejects_malformed_allowlisted_identifiers():
    auth = ToolAuthorizer(
        allowed_tools={
            "official_source_fetch\nshell_exec",
            "official source fetch",
            "official_source_fetch\x00shell_exec",
        }
    )
    for malformed in (
        "official_source_fetch\nshell_exec",
        "official source fetch",
        "official_source_fetch\x00shell_exec",
    ):
        decision = auth.authorize(malformed)
        assert decision.allowed is False
        assert "invalid" in decision.reason.lower()


def test_tool_authorization_cannot_promote_legal_authority_even_when_allowlisted():
    auth = ToolAuthorizer(allowed_tools={"official_source_fetch"})
    denied = auth.authorize(
        "official_source_fetch",
        attempts_authority_promotion=True,
    )
    assert denied.allowed is False
    assert "citationfirewall" in denied.reason.lower()
