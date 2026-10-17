# Architecture — NextLaw607 NY Criminal on Continuity OS

**Companion to:** `docs/nextlaw607-ny-criminal-intelligence.prd.md`

## Problem & goals

NextLaw607 already contains useful legal product code, while Continuity OS Base contains orchestration, RAG, guardrails, routing, memory and software-factory capabilities that should not be independently reimplemented. The architecture must preserve useful NextLaw behavior while moving shared infrastructure behind Continuity OS contracts. The NY criminal vertical must be source-grounded, temporal, auditable and cheap enough to run routinely.

## Approaches considered

### A. Keep NextLaw standalone and copy Continuity features
Fastest superficially, but creates divergent RAG, routing, memory, guardrail and skill implementations. Rejected because drift and duplicated maintenance grow quickly.

### B. Replace NextLaw wholesale with Continuity OS Base
Architecturally clean but risks throwing away working NextLaw UI, legal workflows and existing integrations. Rejected as a blind rewrite.

### C. Incremental convergence — recommended
Treat Continuity OS as the platform/runtime and NextLaw607 as a legal application/pack. Inventory the existing NextLaw code, preserve product surfaces that work, replace duplicated infrastructure behind adapters, and migrate incrementally with parity/regression gates.

## Recommended approach

Use **Continuity OS Base as the shared application/agent foundation** and retain NextLaw607 as its own product repository. NextLaw imports or talks to stable Continuity capabilities through explicit interfaces; it does not fork those capabilities.

The first migration artifact is a **keep / port / replace / retire matrix** for current NextLaw components. No wholesale rewrite occurs before that inventory.

Conceptual layers:

```text
Continuity OS
├─ routing / Jev
├─ token optimizer
├─ skills loader
├─ Archon / agent orchestration
├─ software factory
├─ guardrails / hooks
├─ second brain
├─ generic document parsing + hybrid retrieval
└─ integration adapter framework
          │
          ▼
NextLaw607 legal intelligence
├─ matter workspace
├─ legal corpus adapters
├─ authority normalization
├─ temporal law resolver
├─ legal retrieval/reranking policy
├─ citation graph + treatment evidence
├─ CitationFirewall
├─ Legal War Room
├─ NY criminal modules
├─ role/lens passes
└─ legal UI / work product
```

## Key decisions

### 1. Canonical skills

`coden607/skills` is the canonical source. NextLaw declares required skills; it does not maintain divergent copies.

Always-on engineering/runtime skills:
- compress-token-spend
- route-with-jev
- route-interrupts
- maintain-second-brain
- isolate-agent-runs
- enforce-with-hooks
- run-software-factory
- anticipate

Legal master workflow:
- legal-war-room

Specialized legal skills are composable and narrowly scoped. Role skills are analysis lenses over the same immutable evidence/authority context.

### 2. RAG architecture

Reuse Continuity's generic parsing/chunking/hybrid-search primitives, but add a **legal retrieval policy layer**.

Logical retrieval path:

```text
query/matter
  → issue + jurisdiction/date classification
  → lexical candidate retrieval
  + semantic candidate retrieval
  + citation-neighbor expansion
  → metadata hard filters
  → legal reranker
  → authority hierarchy weighting
  → adverse-authority / prove-me-wrong pass
  → passage-level evidence package
  → CitationFirewall
  → Legal War Room reasoning
```

BM25/lexical retrieval is required because exact citations, statutory language and legal terms are high-value. Semantic retrieval is complementary, not a replacement.

### 3. Authority model

Core logical entities:
- Authority
- AuthorityVersion
- Court
- Jurisdiction
- Citation
- CitationEdge
- TreatmentAssertion
- Passage
- StatuteSection
- Matter
- MatterDocument
- RecordFact
- EvidenceItem
- Witness
- Event
- Issue
- Proposition
- WorkProduct
- RetrievalTrace

Every verified Proposition must point to one or more source Passages. Every TreatmentAssertion must point to the later authority and passage providing the treatment evidence.

### 4. Temporal law

Current-law retrieval is insufficient. Authority/version records carry effective/publication dates and supersession relationships where known. A matter/query may specify an `as_of` date. The resolver must never silently substitute current statutory text when the requested legal date is historical.

### 5. Citation graph / citator

Citation edges are deterministic where citations can be parsed. Treatment classification is evidence-backed and separately confidence-scored. A treatment label is not authoritative merely because a model generated it.

The UI must allow inspection of:
- citing authority;
- cited authority;
- treatment phrase/passages;
- court/date;
- classifier confidence/source;
- human correction where supported.

### 6. CitationFirewall

CitationFirewall sits after retrieval and before a proposition is labeled verified.

Minimum gates:
1. cited source was actually retrieved;
2. source identity/court/date is known;
3. cited passage exists;
4. proposition is entailed/supported by that passage;
5. quotation, if any, matches source;
6. authority hierarchy is correctly described;
7. known negative/superseding treatment is surfaced;
8. unresolved checks downgrade the proposition instead of guessing.

### 7. Record vs law separation

Matter documents and factual evidence use a separate provenance namespace from public legal authority. Retrieval may combine them for reasoning, but the final trace must show whether each proposition is:
- a record fact;
- an inference;
- a legal rule;
- an application of law to fact.

This preserves the Legal War Room record-ledger discipline.

### 8. Role/lens execution

Roles do not get independent mutable memory. The orchestrator builds one frozen case context and dispatches bounded lenses.

Example:
```text
verified context
  ├─ defense lens
  ├─ prosecutor lens
  ├─ trial-judge lens
  └─ appellate lens
       ↓
conflict/issue merger
       ↓
CitationFirewall + critic
       ↓
final work product
```

Additional citizen/security/police/investigator/AG lenses are invoked only when relevant.

### 9. MCP / integration contract

External research providers normalize into an internal result contract conceptually containing:
- provider/source ID;
- authority identity;
- court/jurisdiction;
- date/version;
- canonical citation(s);
- full text or permitted excerpt;
- passage coordinates;
- retrieval timestamp;
- source URL/identifier;
- licensing/usage constraints;
- confidence/verification status.

Initial adapters: CourtListener and official NY legislative sources. Additional commercial providers can be added without changing Legal War Room.

### 10. Security and data boundaries

Public legal corpus data is separate from private matter data. Secrets remain server-side. Autonomous agents receive the smallest matter/context slice needed. External provider calls must not receive private matter content unless the integration and user authorization permit it.

Destructive writes, production deployment, external communication and filing remain explicit approval gates under Continuity OS.

### 11. Token/cost architecture

Token saving is a first-class invariant:
- search before context expansion;
- metadata filters before reranking;
- Jev/deterministic routing before LLM routing;
- cheapest capable model per duty;
- stable cached system/skill prefixes;
- small passage windows instead of full opinions where sufficient;
- batch compatible retrieval/classification;
- deduplicate authorities/passages;
- 10% judge sampling for routine quality telemetry, with 100% deterministic CitationFirewall checks;
- frontier models reserved for genuinely complex synthesis;
- record token, cost, latency and route per workflow.

Legal correctness gates are not disabled to save tokens.

### 12. Software factory

The engineering path is:

```text
PRD
 → architecture
 → migration inventory
 → vertical slices/issues
 → isolated implementation branches/worktrees
 → unit/integration/legal-eval gates
 → critic/verifier
 → PR
 → human merge/deploy approval
```

The factory may automate reversible development work within configured autonomy. It must not silently raise autonomy or perform protected external/destructive actions.

## Keep / Port / Replace inventory categories

Before implementation, classify each current NextLaw subsystem:

| Category | Meaning |
|---|---|
| KEEP | Product-specific code remains in NextLaw with minimal change |
| PORT | Useful behavior moves behind a Continuity/NextLaw interface |
| REPLACE | Duplicate infrastructure is replaced by a Continuity capability |
| RETIRE | Dead/Grok-specific or superseded code removed only after parity |
| SPIKE | Unclear/risky; test before deciding |

Initial hypotheses, not final inventory:
- legal UI/matter workflow → KEEP/PORT;
- verified legal corpus logic → KEEP then normalize;
- generic RAG primitives → REPLACE with Continuity primitives where parity exists;
- generic model routing → REPLACE with Continuity/Jev;
- legal hierarchy/CitationFirewall → KEEP/EXPAND in NextLaw;
- Grok-specific scaffolding → SPIKE/RETIRE only after dependency audit.

## Missing pieces

- completed keep/port/replace inventory;
- normalized authority schema;
- temporal statute/version ingestion;
- legal metadata filters/reranker;
- citation parser and graph;
- evidence-backed treatment classifier;
- CitationFirewall proposition verifier;
- legal evaluation/holdout suite;
- NY criminal specialized skills;
- provider capability/licensing matrix;
- private-matter data retention/encryption policy;
- UI for provenance, authority hierarchy and treatment inspection.

## Spikes & experiments

### Spike 1 — migration compatibility
**Question:** Can Continuity OS Base replace generic NextLaw orchestration/RAG without losing existing behavior?  
**Spike:** run one representative existing NextLaw research workflow through both paths.  
**Decision rule:** migrate a component only when parity or improvement is demonstrated and legal provenance is preserved.

### Spike 2 — legal hybrid retrieval
**Question:** Does Continuity generic hybrid retrieval achieve acceptable legal recall?  
**Spike:** benchmark lexical-only, semantic-only and hybrid+rereank on a small NY criminal gold set.  
**Decision rule:** select the cheapest configuration meeting the recall/precision target.

### Spike 3 — treatment classification
**Question:** Can treatment labels be shown reliably?  
**Spike:** hand-label a stratified later-citing case set and compare deterministic cues + model classification.  
**Decision rule:** labels below the validated precision threshold remain evidence-only/uncertain rather than categorical.

### Spike 4 — historical law
**Question:** Can reliable historical statutory versions/effective dates be sourced?  
**Spike:** trace a sample of materially amended Penal Law/CPL sections across dates.  
**Decision rule:** no law-as-of feature graduates until version provenance is reproducible.

## Open questions

- exact deployment boundary between Continuity daemon/library and NextLaw app;
- database/vector backend for production scale;
- canonical historical-law source;
- provider/licensing limits;
- treatment accuracy threshold;
- expert validation process and gold-set ownership;
- private matter retention/encryption requirements;
- whether existing Grok-derived UI should be progressively migrated or retained long term.

## Architectural decision

Adopt **incremental convergence**: Continuity OS supplies shared agent/application infrastructure; NextLaw607 owns legal-domain intelligence. Build NY criminal depth first, measure it, then expand.
