from __future__ import annotations


def test_mem0_runtime_exposes_required_memory_client_operations():
    from mem0 import MemoryClient

    for operation in ("add", "get_all", "delete"):
        assert callable(getattr(MemoryClient, operation, None)), operation
