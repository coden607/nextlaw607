from pathlib import Path


def test_mem0_provider_release_gate_requires_real_service_and_exact_revision_evidence():
    workflow = Path(".github/workflows/mem0-live-smoke.yml")
    assert workflow.exists(), "Mem0 cannot be promoted without a provider-backed live smoke workflow"

    text = workflow.read_text(encoding="utf-8")
    assert "MEM0_API_KEY" in text
    assert "NEXTLAW_EXACT_REVISION" in text
    assert "compat/test_mem0_live_smoke.py" in text
    assert "mem0-live-evidence" in text
    assert "actions/upload-artifact@v4" in text


def test_mem0_provider_workflow_is_controlled_manual_gate():
    workflow = Path(".github/workflows/mem0-live-smoke.yml")
    text = workflow.read_text(encoding="utf-8")
    trigger_section = text.split("permissions:", 1)[0]

    assert "workflow_dispatch:" in trigger_section
    assert "\n  push:" not in trigger_section
    assert "\n  pull_request:" not in trigger_section


def test_mem0_provider_live_smoke_must_prove_scope_delete_and_requery_through_adapter():
    smoke = Path("compat/test_mem0_live_smoke.py")
    assert smoke.exists(), "provider-backed Mem0 add/read/delete/re-query evidence is required"

    text = smoke.read_text(encoding="utf-8")
    for required in (
        "MemoryClient",
        "Mem0MemoryAdapter",
        "NEXTLAW_MEM0_TEST_SCOPE",
        "adapter.remember(",
        "adapter.export(",
        "adapter.delete(",
        "authority_eligible",
        "memory_can_verify_authority",
        "mem0-live-evidence.json",
    ):
        assert required in text, required
