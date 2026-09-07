-- NextLaw607 authoritative entitlement store.
--
-- This table is intentionally backend-only. Browser clients authenticate through
-- Supabase Auth, but paid access is resolved by the NextLaw API from this
-- authoritative table using a server-held service-role/secret credential.
-- No anon/authenticated table policy is created here.

create table if not exists public.entitlements (
    user_id uuid primary key references auth.users(id) on delete cascade,
    tier text not null,
    source text not null,
    expires_at timestamptz null,
    revocable boolean not null default true,
    billing_required boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint entitlements_tier_allowed check (
        tier in ('free', 'premium', 'case_pass', 'pro', 'institutional')
    ),
    constraint entitlements_source_allowed check (
        source in ('purchase', 'institutional_grant', 'founder_lifetime_grant')
    ),
    constraint entitlements_founder_invariant check (
        source <> 'founder_lifetime_grant'
        or (
            tier = 'premium'
            and expires_at is null
            and revocable = false
            and billing_required = false
        )
    ),
    constraint entitlements_institutional_tier check (
        source <> 'institutional_grant'
        or tier = 'institutional'
    )
);

comment on table public.entitlements is
    'Authoritative server-only NextLaw607 access grants. Never derive authorization from auth user_metadata.';

alter table public.entitlements enable row level security;

-- Explicit least privilege for Data API roles. RLS alone is not the grant layer.
revoke all on table public.entitlements from public;
revoke all on table public.entitlements from anon;
revoke all on table public.entitlements from authenticated;

-- Backend entitlement resolution only. service_role bypasses RLS and must remain
-- server-side; it is never shipped to browser/PWA code. Read and write grants are
-- kept separate so the authorization surface is obvious during review.
grant select on table public.entitlements to service_role;
grant insert, update, delete on table public.entitlements to service_role;
