from __future__ import annotations

import os
from pathlib import Path

import psycopg
import pytest


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "202609080001_legal_chunks_pgvector.sql"
DSN = os.environ.get("NEXTLAW_PGVECTOR_TEST_DSN", "postgresql://postgres:postgres@127.0.0.1:5432/postgres")


def _connect(role: str, password: str = "postgres"):
    return psycopg.connect(f"postgresql://{role}:{password}@127.0.0.1:5432/postgres")


def test_pgvector_migration_enforces_rls_and_service_role_retrieval():
    with psycopg.connect(DSN, autocommit=True) as admin:
        admin.execute("drop schema if exists public cascade")
        admin.execute("create schema public")
        admin.execute("grant all on schema public to postgres")
        for role in ("anon", "authenticated", "service_role"):
            admin.execute(f"drop role if exists {role}")
        admin.execute("create role anon login password 'postgres' nobypassrls")
        admin.execute("create role authenticated login password 'postgres' nobypassrls")
        admin.execute("create role service_role login password 'postgres' bypassrls")
        admin.execute(MIGRATION.read_text(encoding="utf-8"))

        zero = "[" + ",".join(["0"] * 1536) + "]"
        one = "[1," + ",".join(["0"] * 1535) + "]"
        admin.execute(
            """
            insert into public.legal_chunks
              (source_url, jurisdiction, content, content_sha256, embedding)
            values
              ('https://example.test/ny-a', 'NY', 'verified-candidate-a', %s, %s::vector),
              ('https://example.test/ny-b', 'NY', 'verified-candidate-b', %s, %s::vector),
              ('https://example.test/pa', 'PA', 'other-jurisdiction', %s, %s::vector)
            """,
            ("a" * 64, zero, "b" * 64, one, "c" * 64, zero),
        )

    for role in ("anon", "authenticated"):
        with _connect(role) as conn:
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                conn.execute("select count(*) from public.legal_chunks").fetchone()
            conn.rollback()
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                conn.execute(
                    "select * from public.match_legal_chunks(%s::vector, 8, 'NY')",
                    ("[" + ",".join(["0"] * 1536) + "]",),
                ).fetchall()

    with _connect("service_role") as conn:
        rows = conn.execute(
            "select jurisdiction, source_url, similarity from public.match_legal_chunks(%s::vector, 8, 'NY')",
            ("[" + ",".join(["0"] * 1536) + "]",),
        ).fetchall()

    assert rows
    assert all(row[0] == "NY" for row in rows)
    assert all(row[1].startswith("https://") for row in rows)
    assert len(rows) == 2
