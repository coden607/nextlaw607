def test_nemo_guardrails_runtime_imports():
    import nemoguardrails  # noqa: F401
    from nemoguardrails import RailsConfig  # noqa: F401


def test_nextlaw_deterministic_guardrail_remains_authoritative_boundary():
    from nextlaw607.guardrails import GuardrailGate, ToolAuthorizer

    assert GuardrailGate().inspect_input("ordinary legal research question").allowed is True
    assert ToolAuthorizer(allowed_tools={"official_source_fetch"}).authorize("shell_exec").allowed is False
