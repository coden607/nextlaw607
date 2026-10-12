# NextLaw607 pgvector Retrieval Milestone

**Parent plan:** `docs/superpowers/plans/2026-09-07-production-stack.md`

**Goal:** Add production pgvector persistence/retrieval without allowing semantic similarity, stored chunks, memory, or model output to become legal evidence.

## Completed

- [x] RED: retrieval tests failed because `nextlaw607.retrieval` did not exist.
- [x] RED: schema contract required pgvector extension, 1536-dimensional vectors, RLS, service-role ownership, and a server-only RPC.
- [x] Implement `SupabasePgvectorRepository` using HTTPS-only server credentials and bounded 1536-dimensional finite embeddings.
- [x] Fail closed on transport errors, non-200 responses, malformed rows, unsafe URLs, jurisdiction mismatch, invalid hashes, oversized content, or invalid similarity values.
- [x] Make `RetrievedChunk.trusted`, `verified_authority`, and `authority_eligible` immutable non-init false fields so callers cannot self-promote retrieved text.
- [x] Add `legal_chunks` pgvector schema, cosine HNSW index, RLS/forced RLS, revoked anon/authenticated access, and service-role-only `match_legal_chunks` RPC.
- [x] Add a controlled PostgreSQL + pgvector live-smoke lane that models Supabase `anon`, `authenticated`, and `service_role` access and proves denied public reads/RPC execution plus ranked service-role retrieval.
- [x] Exact-revision CI run `34214649558` passed on `3531d64c79390a256946b9101d182491b7c11b7f`.
- [x] Browser release evidence run `34214649521` passed on the same revision.
- [x] Record the exact smoke/CI/browser evidence in `config/production-stack.json`.

## Remaining hosted-environment verification gate

- [ ] Apply the migration to a controlled hosted Supabase test project with pgvector enabled.
- [ ] Insert known synthetic chunks through server credentials only.
- [ ] Prove hosted anon/authenticated direct reads and RPC execution are denied.
- [ ] Prove hosted service-role semantic search returns ranked candidates with exact provenance while all trust flags remain false.
- [ ] Only after the hosted Supabase checks pass, promote pgvector from `implemented` to `verified`.

## Legal-trust invariant

Vector similarity is discovery/ranking only. Any proposition intended for citation must independently become a `LegalAuthority` and pass `CitationFirewall`; retrieval scores never affect authority status.
