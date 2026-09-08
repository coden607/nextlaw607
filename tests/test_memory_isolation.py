from __future__ import annotations

from nextlaw607.memory import MemoryScope, MemoryVault, memory_can_verify_authority


def test_memory_requires_explicit_consent_before_persisting():
    vault = MemoryVault()
    scope = MemoryScope(user_id="user-1", case_id="case-a", agent_id="research", session_id="session-1")

    try:
        vault.remember("client prefers concise answers", scope=scope, consent=False)
    except PermissionError as exc:
        assert "consent" in str(exc).lower()
    else:
        raise AssertionError("memory persistence without consent must fail closed")


def test_memory_isolated_by_user_case_agent_and_session():
    vault = MemoryVault()
    scope_a = MemoryScope("user-1", "case-a", "research", "session-1")
    scope_b = MemoryScope("user-1", "case-b", "research", "session-1")

    vault.remember("fact for case a", scope=scope_a, consent=True)
    vault.remember("fact for case b", scope=scope_b, consent=True)

    exported_a = vault.export(scope_a)
    exported_b = vault.export(scope_b)

    assert [item.content for item in exported_a] == ["fact for case a"]
    assert [item.content for item in exported_b] == ["fact for case b"]


def test_memory_redacts_common_secrets_before_storage():
    vault = MemoryVault()
    scope = MemoryScope("user-1", "case-a", "research", "session-1")

    record = vault.remember(
        "Bearer abc.def.ghi and sk-test-1234567890 should never be stored",
        scope=scope,
        consent=True,
    )

    assert "abc.def.ghi" not in record.content
    assert "sk-test-1234567890" not in record.content
    assert "[REDACTED]" in record.content


def test_export_and_delete_are_exact_scope_operations():
    vault = MemoryVault()
    scope_a = MemoryScope("user-1", "case-a", "research", "session-1")
    scope_b = MemoryScope("user-1", "case-a", "research", "session-2")
    vault.remember("session one", scope=scope_a, consent=True)
    vault.remember("session two", scope=scope_b, consent=True)

    deleted = vault.delete(scope_a)

    assert deleted == 1
    assert vault.export(scope_a) == ()
    assert [item.content for item in vault.export(scope_b)] == ["session two"]


def test_memory_can_never_become_legal_authority():
    vault = MemoryVault()
    scope = MemoryScope("user-1", "case-a", "research", "session-1")
    record = vault.remember("People v Example supposedly says X", scope=scope, consent=True)

    assert record.authority_eligible is False
    assert memory_can_verify_authority(record) is False
