import os
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest


DSN_ENV = "NEXTLAW_SUPABASE_TEST_DSN"
MIGRATIONS = Path("supabase/migrations")
ENTITLEMENT_MIGRATIONS = (
    MIGRATIONS / "202609070001_entitlements.sql",
    MIGRATIONS / "20260907_nextlaw_entitlements.sql",
)


@pytest.fixture()
def db():
    dsn = os.environ.get(DSN_ENV)
    if not dsn:
        pytest.skip(f"{DSN_ENV} is required for the live Supabase/Postgres smoke")

    with psycopg.connect(dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("drop table if exists public.entitlements cascade")
            cur.execute("drop schema if exists auth cascade")
            for role in ("anon", "authenticated", "service_role"):
                cur.execute(f"drop role if exists {role}")
            cur.execute("create role anon nologin")
            cur.execute("create role authenticated nologin")
            # Supabase service_role bypasses RLS; mirror that server-only property.
            cur.execute("create role service_role nologin bypassrls")
            cur.execute("create schema auth")
            cur.execute("create table auth.users (id uuid primary key)")

        for migration in ENTITLEMENT_MIGRATIONS:
            conn.execute(migration.read_text(encoding="utf-8"))

        yield conn

        with conn.cursor() as cur:
            cur.execute("reset role")
            cur.execute("drop table if exists public.entitlements cascade")
            cur.execute("drop schema if exists auth cascade")
            for role in ("anon", "authenticated", "service_role"):
                cur.execute(f"drop role if exists {role}")


def _has_table_privilege(conn, role: str, privilege: str) -> bool:
    return bool(
        conn.execute(
            "select has_table_privilege(%s, 'public.entitlements', %s)",
            (role, privilege),
        ).fetchone()[0]
    )


def test_entitlements_schema_executes_with_forced_rls_and_least_privilege(db):
    relrowsecurity, relforcerowsecurity = db.execute(
        "select relrowsecurity, relforcerowsecurity "
        "from pg_class where oid = 'public.entitlements'::regclass"
    ).fetchone()
    assert relrowsecurity is True
    assert relforcerowsecurity is True

    for role in ("anon", "authenticated"):
        for privilege in ("SELECT", "INSERT", "UPDATE", "DELETE"):
            assert _has_table_privilege(db, role, privilege) is False

    for privilege in ("SELECT", "INSERT", "UPDATE", "DELETE"):
        assert _has_table_privilege(db, "service_role", privilege) is True

    policies = db.execute(
        "select count(*) from pg_policies where schemaname='public' and tablename='entitlements'"
    ).fetchone()[0]
    assert policies == 0


def test_founder_entitlement_contract_is_enforced_by_postgres(db):
    user_id = uuid4()
    db.execute("insert into auth.users(id) values (%s)", (user_id,))

    with db.transaction():
        db.execute("set local role service_role")
        db.execute(
            "insert into public.entitlements "
            "(user_id, tier, source, expires_at, revocable, billing_required) "
            "values (%s, 'premium', 'founder_lifetime_grant', null, false, false)",
            (user_id,),
        )

    invalid_user_id = uuid4()
    db.execute("insert into auth.users(id) values (%s)", (invalid_user_id,))
    with pytest.raises(psycopg.errors.CheckViolation):
        with db.transaction():
            db.execute("set local role service_role")
            db.execute(
                "insert into public.entitlements "
                "(user_id, tier, source, expires_at, revocable, billing_required) "
                "values (%s, 'pro', 'founder_lifetime_grant', null, false, false)",
                (invalid_user_id,),
            )
