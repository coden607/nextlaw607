# Legal Platform Parity Architecture

## Core rule

RAG is part of the retrieval stack, not the legal-truth layer.

```
official/public sources
  -> source registry + rights/provenance
  -> immutable raw snapshots
  -> parsing/normalization
  -> canonical legal IDs + versions
  -> chunks/passages
  -> lexical index + vector index + metadata index
  -> citation graph / treatment graph
  -> hybrid retrieval + graph expansion
  -> research/drafting agents
  -> CitationFirewall / quote verifier / citator checks
  -> user-facing answer or draft
```

## Data planes

### 1. Source plane

Stores source registry, source class, official/repository status, allowed use, jurisdiction, parser, fetch cadence, last success/failure, and retention policy.

### 2. Immutable document plane

Stores raw legal text and metadata by content hash. Never destructively mutate a prior legal version; create a new version and lineage edge.

### 3. Canonical legal-entity plane

Stable IDs for cases, opinions, statutes, statutory sections, rules, regulations, dockets, and filings. Aliases/parallel citations point to the same canonical entity.

### 4. Passage plane

Chunked passages contain document ID, source hash, section/page/paragraph/span anchors, jurisdiction, court, date, legal entity IDs, and embedding version.

### 5. Search plane

Use:
- PostgreSQL/tsvector or equivalent lexical search.
- pgvector semantic search.
- metadata filters.
- reciprocal-rank or learned fusion evaluated offline.
- citation-graph expansion.

Do not use vector similarity as authority weight.

### 6. Citation/treatment graph

Nodes are canonical legal entities. Edges carry citation relation, treatment label, explicit/inferred status, confidence, evidence span, source, reviewer status, and temporal applicability.

### 7. Matter plane

Separate from the public legal corpus. Tenant/user/matter scoped documents, facts, timeline, notes, drafts, checkpoints, work product, and permissions. Matter text must never leak into public corpus indexes or routing telemetry.

### 8. Agent plane

Research, drafting, document, chronology, citator, and critic agents consume only bounded, provenance-rich context. Deterministic classification/routing runs first. Agents cannot self-mark authority verified.

## Retrieval pipeline

1. Classify issue/jurisdiction/posture.
2. Build bounded query set.
3. Run lexical search.
4. Run semantic search.
5. Apply metadata constraints.
6. Fuse ranks.
7. Expand citation neighbors.
8. Re-rank by legal hierarchy, temporal applicability, and issue fit.
9. Run adverse-authority pass.
10. Verify source/citator state.
11. Build context with provenance and token budget.
12. Synthesize.
13. Validate every citation/quote/proposition before release.

## Database direction

Supabase/Postgres remains a good fit for the first stages because it can hold relational metadata, RLS, JSONB, tsvector, and pgvector together. Use specialized external search/graph infrastructure only when measured scale/latency justifies it.

Likely logical tables:

- legal_sources
- source_snapshots
- legal_documents
- legal_document_versions
- legal_passages
- canonical_legal_entities
- citation_aliases
- citation_edges
- treatment_evidence
- ingestion_jobs
- embedding_versions
- corpus_coverage
- matters
- matter_documents
- matter_facts
- matter_events
- matter_authorities
- matter_drafts
- review_events

## Verification boundary

Retrieved text is evidence/candidate context. A LegalAuthority becomes citable only after CitationFirewall requirements are satisfied. Quoted language additionally requires exact source-span verification.

## Scaling triggers

Do not add a separate vector DB, search cluster, or graph DB merely for parity optics. Introduce one only after benchmarks show Postgres cannot meet the declared corpus size, update rate, query latency, graph traversal, or operational-reliability target.
