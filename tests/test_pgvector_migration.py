from pathlib import Path


def test_pgvector_migration_is_server_owned_rls_and_vector_enabled():
    sql = Path("supabase/migrations/202609080001_legal_chunks_pgvector.sql").read_text()
    normalized = " ".join(sql.lower().split())

    assert "create extension if not exists vector" in normalized
    assert "embedding vector(1536)" in normalized
    assert "enable row level security" in normalized
    assert "match_legal_chunks" in normalized
    assert "security invoker" in normalized
    assert "revoke all on" in normalized
    assert "anon" in normalized
    assert "authenticated" in normalized
    assert "service_role" in normalized
    assert "jurisdiction" in normalized
    assert "content_sha256" in normalized
