create extension if not exists vector;

create table if not exists public.legal_chunks (
  id uuid primary key default gen_random_uuid(),
  source_url text not null check (source_url like 'https://%'),
  jurisdiction text not null check (length(jurisdiction) between 1 and 64),
  content text not null check (length(content) between 1 and 200000),
  content_sha256 char(64) not null check (content_sha256 ~ '^[0-9a-fA-F]{64}$'),
  embedding vector(1536) not null,
  created_at timestamptz not null default now(),
  unique (source_url, content_sha256)
);

alter table public.legal_chunks enable row level security;
alter table public.legal_chunks force row level security;

revoke all on table public.legal_chunks from public, anon, authenticated;
grant select, insert, update, delete on table public.legal_chunks to service_role;

create index if not exists legal_chunks_jurisdiction_idx
  on public.legal_chunks (jurisdiction);

create index if not exists legal_chunks_embedding_hnsw_idx
  on public.legal_chunks using hnsw (embedding vector_cosine_ops);

create or replace function public.match_legal_chunks(
  query_embedding vector(1536),
  match_count integer default 8,
  filter_jurisdiction text default null
)
returns table (
  id uuid,
  source_url text,
  jurisdiction text,
  content text,
  content_sha256 char(64),
  similarity double precision
)
language sql
stable
security invoker
set search_path = public
as $$
  select
    lc.id,
    lc.source_url,
    lc.jurisdiction,
    lc.content,
    lc.content_sha256,
    1 - (lc.embedding <=> query_embedding) as similarity
  from public.legal_chunks as lc
  where filter_jurisdiction is null or lc.jurisdiction = filter_jurisdiction
  order by lc.embedding <=> query_embedding
  limit least(greatest(coalesce(match_count, 8), 1), 20);
$$;

revoke all on function public.match_legal_chunks(vector, integer, text)
  from public, anon, authenticated;
grant execute on function public.match_legal_chunks(vector, integer, text)
  to service_role;
