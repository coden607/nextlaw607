from pathlib import Path


MIGRATION = Path('supabase/migrations/20260907_nextlaw_entitlements.sql')


def migration_sql() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_entitlement_migration_exists_and_targets_public_entitlements():
    sql = migration_sql()
    assert 'create table' in sql
    assert 'public.entitlements' in sql
    assert 'user_id uuid primary key' in sql
    assert 'references auth.users(id)' in sql


def test_entitlement_migration_enforces_allowed_tiers_and_sources():
    sql = migration_sql()
    for value in ('free', 'premium', 'case_pass', 'pro', 'institutional'):
        assert f"'{value}'" in sql
    for value in ('purchase', 'institutional_grant', 'founder_lifetime_grant'):
        assert f"'{value}'" in sql


def test_founder_grant_cannot_be_weakened_in_storage():
    sql = migration_sql()
    assert 'founder_lifetime_grant' in sql
    assert "tier = 'premium'" in sql
    assert 'expires_at is null' in sql
    assert 'revocable = false' in sql or 'not revocable' in sql
    assert 'billing_required = false' in sql or 'not billing_required' in sql


def test_entitlements_enable_rls_and_revoke_client_table_privileges():
    sql = migration_sql()
    assert 'enable row level security' in sql
    assert 'revoke all on table public.entitlements from anon' in sql
    assert 'revoke all on table public.entitlements from authenticated' in sql


def test_entitlements_do_not_define_direct_client_rls_policies():
    sql = migration_sql()
    assert 'create policy' not in sql
    assert 'auth.uid()' not in sql


def test_service_role_is_the_only_explicit_data_reader():
    sql = migration_sql()
    assert 'grant select on table public.entitlements to service_role' in sql
    assert 'grant select on table public.entitlements to anon' not in sql
    assert 'grant select on table public.entitlements to authenticated' not in sql
