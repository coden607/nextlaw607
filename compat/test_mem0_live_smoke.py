from __future__ import annotations

import json
import os
import time
from pathlib import Path
from uuid import uuid4

from mem0 import MemoryClient

from nextlaw607.memory import Mem0MemoryAdapter, MemoryScope, memory_can_verify_authority


def _wait_for_export(adapter: Mem0MemoryAdapter, scope: MemoryScope, *, present: bool, timeout: float = 60.0):
    deadline = time.monotonic() + timeout
    latest = ()
    while time.monotonic() < deadline:
        latest = adapter.export(scope)
        if bool(latest) is present:
            return latest
        time.sleep(2.0)
    return latest


def test_mem0_provider_add_scope_delete_and_requery():
    api_key = os.environ.get("MEM0_API_KEY", "").strip()
    revision = os.environ.get("NEXTLAW_EXACT_REVISION", "").strip()
    scope_prefix = os.environ.get("NEXTLAW_MEM0_TEST_SCOPE", "").strip()
    if not api_key:
        raise AssertionError("MEM0_API_KEY is required for provider-backed verification")
    if not revision:
        raise AssertionError("NEXTLAW_EXACT_REVISION is required")
    if not scope_prefix:
        raise AssertionError("NEXTLAW_MEM0_TEST_SCOPE is required")

    suffix = uuid4().hex
    primary = MemoryScope(
        user_id=f"{scope_prefix}-user-{suffix}",
        case_id=f"{scope_prefix}-case-a-{suffix}",
        agent_id=f"{scope_prefix}-agent-{suffix}",
        session_id=f"{scope_prefix}-run-{suffix}",
    )
    adjacent = MemoryScope(
        user_id=primary.user_id,
        case_id=f"{scope_prefix}-case-b-{suffix}",
        agent_id=primary.agent_id,
        session_id=primary.session_id,
    )

    client = MemoryClient(api_key=api_key)
    adapter = Mem0MemoryAdapter(client)
    created_ids: set[str] = set()
    evidence = {
        "schema_version": 1,
        "revision": revision,
        "provider": "mem0-platform",
        "authority_eligible": False,
        "scope_isolation": False,
        "delete_count": 0,
        "requery_empty": False,
    }

    try:
        primary_record = adapter.remember(
            "NextLaw provider isolation probe alpha",
            scope=primary,
            consent=True,
        )
        adjacent_record = adapter.remember(
            "NextLaw provider isolation probe beta",
            scope=adjacent,
            consent=True,
        )
        created_ids.update((primary_record.memory_id, adjacent_record.memory_id))

        primary_records = _wait_for_export(adapter, primary, present=True)
        adjacent_records = _wait_for_export(adapter, adjacent, present=True)
        assert primary_records, "primary Mem0 scope did not become readable"
        assert adjacent_records, "adjacent Mem0 scope did not become readable"
        assert all(record.scope == primary for record in primary_records)
        assert all(record.authority_eligible is False for record in primary_records)
        assert all(memory_can_verify_authority(record) is False for record in primary_records)
        assert all("probe beta" not in record.content for record in primary_records)
        assert all("probe alpha" not in record.content for record in adjacent_records)
        evidence["scope_isolation"] = True

        deleted = adapter.delete(primary)
        evidence["delete_count"] = deleted
        assert deleted >= 1
        after_delete = _wait_for_export(adapter, primary, present=False)
        assert after_delete == ()
        evidence["requery_empty"] = True
    finally:
        for scope in (primary, adjacent):
            try:
                adapter.delete(scope)
            except Exception:
                pass
        Path("mem0-live-evidence.json").write_text(
            json.dumps(evidence, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    assert evidence["scope_isolation"] is True
    assert evidence["requery_empty"] is True
