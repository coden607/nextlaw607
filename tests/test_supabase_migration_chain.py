from pathlib import Path


MIGRATIONS = Path("supabase/migrations")


def entitlement_migrations() -> list[Path]:
    return sorted(path for path in MIGRATIONS.glob("*.sql") if "entitlement" in path.name)


def test_entitlement_schema_has_single_create_table_source_of_truth():
    creators = []
    for path in entitlement_migrations():
        sql = path.read_text(encoding="utf-8").lower()
        if "create table if not exists public.entitlements" in sql:
            creators.append(path.name)
    assert creators == ["202609070001_entitlements.sql"]


def test_entitlement_migration_chain_matches_founder_runtime_contract():
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower() for path in entitlement_migrations()
    )
    assert "founder_lifetime_grant" in combined
    assert "tier = 'premium'" in combined
    assert "tier = 'pro'" not in combined
    assert "expires_at is null" in combined
    assert "revocable = false" in combined
    assert "billing_required = false" in combined


def test_entitlement_chain_preserves_fail_closed_client_access():
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower() for path in entitlement_migrations()
    )
    assert "enable row level security" in combined
    assert "force row level security" in combined
    assert "revoke all on table public.entitlements from anon" in combined
    assert "revoke all on table public.entitlements from authenticated" in combined
    assert "grant select on table public.entitlements to service_role" in combined
    assert "grant select on table public.entitlements to anon" not in combined
    assert "grant select on table public.entitlements to authenticated" not in combined
