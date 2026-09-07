begin;

create table if not exists public.entitlements (
  user_id uuid primary key references auth.users(id) on delete cascade,
  tier text not null check (tier in ('premium', 'case_pass', 'pro', 'institutional')),
  source text not null check (source in ('purchase', 'institutional_grant', 'founder_lifetime_grant')),
  expires_at timestamptz null,
  revocable boolean not null,
  billing_required boolean not null,
  updated_at timestamptz not null default now(),
  constraint founder_lifetime_canonical check (
    source <> 'founder_lifetime_grant'
    or (tier = 'pro' and expires_at is null and revocable = false and billing_required = false)
  )
);

alter table public.entitlements enable row level security;
alter table public.entitlements force row level security;

-- No anon/authenticated policies are created: direct client access fails closed.
revoke all on table public.entitlements from anon, authenticated;
grant select, insert, update, delete on table public.entitlements to service_role;

comment on table public.entitlements is
  'Server-authoritative NextLaw607 access grants. Client metadata is never authorization.';

commit;
