-- NextLaw607 entitlement hardening follow-up.
--
-- The canonical table definition lives in 202609070001_entitlements.sql.
-- This migration intentionally does not redefine public.entitlements. It only
-- reasserts the backend-only authorization boundary so a clean migration chain
-- has one schema source of truth and direct browser roles remain fail closed.

alter table public.entitlements enable row level security;
alter table public.entitlements force row level security;

revoke all on table public.entitlements from public;
revoke all on table public.entitlements from anon;
revoke all on table public.entitlements from authenticated;

grant select on table public.entitlements to service_role;
grant insert, update, delete on table public.entitlements to service_role;

comment on table public.entitlements is
    'Authoritative server-only NextLaw607 access grants. Never derive authorization from auth user_metadata.';
