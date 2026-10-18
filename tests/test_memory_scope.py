from nextlaw607.execution_state import RunScope
from nextlaw607.memory_scope import MatterMemoryStore, MemoryScope


def test_memory_scope_aligns_with_run_scope():
    run = RunScope("u1", "matter-a", "research", "run-1")
    assert MemoryScope.from_run_scope(run) == MemoryScope("u1", "matter-a")


def test_memory_isolated_by_matter():
    store = MatterMemoryStore()
    a = MemoryScope("u1", "matter-a")
    b = MemoryScope("u1", "matter-b")
    store.put(a, "phase", "research")
    assert store.get(a, "phase") == "research"
    assert store.get(b, "phase") is None


def test_memory_never_promotes_authority():
    assert MatterMemoryStore.authority_eligible() is False
