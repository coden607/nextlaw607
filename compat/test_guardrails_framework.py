from pathlib import Path


def test_nemo_guardrails_runtime_imports():
    import nemoguardrails  # noqa: F401
    from nemoguardrails import RailsConfig  # noqa: F401


def test_committed_nemo_guardrails_config_loads_in_guardrails_runtime():
    from nextlaw607.guardrails import NemoGuardrailsAdapter

    decision = NemoGuardrailsAdapter().configured_runtime_status(Path("config/nemo"))

    assert decision.allowed is True
    assert decision.reason == "NeMo Guardrails configured runtime available"


def test_nextlaw_deterministic_guardrail_remains_authoritative_boundary():
    from nextlaw607.guardrails import GuardrailGate, ToolAuthorizer

    assert GuardrailGate().inspect_input("ordinary legal research question").allowed is True
    assert ToolAuthorizer(allowed_tools={"official_source_fetch"}).authorize("shell_exec").allowed is False
