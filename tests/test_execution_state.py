from __future__ import annotations

import pytest

from nextlaw607.execution_state import (
    Checkpoint,
    CheckpointStore,
    RunScope,
    checkpoint_can_verify_authority,
)


def test_run_scope_is_exact_and_opaque():
    a = RunScope("u1", "matter-a", "research", "run-1")
    b = RunScope("u1", "matter-b", "research", "run-1")
    assert a.namespace != b.namespace
    assert "matter-a" not in a.namespace


def test_wildcard_scope_fails_closed():
    with pytest.raises(ValueError):
        RunScope("u1", "*", "research", "run-1")


def test_checkpoint_is_exact_scope_and_never_authority(tmp_path):
    store = CheckpointStore(tmp_path)
    scope = RunScope("u1", "matter-a", "research", "run-1")
    cp = Checkpoint(scope, "collect", 1, {"cursor": 4})
    store.save(cp, expected_revision=0)
    loaded = store.load(scope)
    assert loaded == cp
    assert checkpoint_can_verify_authority(loaded) is False


def test_checkpoint_revision_conflict_prevents_lost_update(tmp_path):
    store = CheckpointStore(tmp_path)
    scope = RunScope("u1", "matter-a", "research", "run-1")
    store.save(Checkpoint(scope, "collect", 1, {}), expected_revision=0)
    with pytest.raises(RuntimeError):
        store.save(Checkpoint(scope, "verify", 2, {}), expected_revision=0)


def test_checkpoint_revision_must_increment_exactly_once(tmp_path):
    store = CheckpointStore(tmp_path)
    scope = RunScope("u1", "matter-a", "research", "run-1")
    with pytest.raises(ValueError):
        store.save(Checkpoint(scope, "collect", 2, {}), expected_revision=0)


def test_other_run_cannot_read_checkpoint(tmp_path):
    store = CheckpointStore(tmp_path)
    first = RunScope("u1", "matter-a", "research", "run-1")
    second = RunScope("u1", "matter-a", "research", "run-2")
    store.save(Checkpoint(first, "collect", 1, {"cursor": 1}), expected_revision=0)
    assert store.load(second) is None
