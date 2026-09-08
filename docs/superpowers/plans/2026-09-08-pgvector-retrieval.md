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
- [x] Record pgvector as `implemented` in `config/production-stack.json` with implementation/test evidence.

## Remaining verification gate

- [ ] Apply the migration to a controlled Supabase test project with pgvector enabled.
- [ ] Insert known synthetic chunks through server credentials only.
- [ ] Prove anon/authenticated direct reads and RPC execution are denied.
- [ ] Prove service-role semantic search returns ranked candidates with exact provenance while all trust flags remain false.
- [ ] Re-run exact-revision CI/security/legal/privacy gates and only then promote pgvector from `implemented` to `verified`.

## Legal-trust invariant

Vector similarity is discovery/ranking only. Any proposition intended for citation must independently become a `LegalAuthority` and pass `CitationFirewall`; retrieval scores never affect authority status.
