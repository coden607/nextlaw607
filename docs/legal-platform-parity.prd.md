# NextLaw607 — Legal Research & AI Platform Parity PRD

Status: active product direction  
Primary market: New York criminal-law research and litigation workflow first  
North star: functional day-to-day comparability with Westlaw + CoCounsel and Lexis+ + Protégé for the selected scope, without claiming proprietary editorial identity or corpus ownership.

## Product thesis

NextLaw607 should become a legal intelligence system in which attorneys can search law without chat, run source-backed deep research, analyze matter documents, draft litigation work product, test adverse authority, verify every citation and quotation, maintain a secure matter workspace, and export reproducible research/drafting artifacts.

The moat is not a chatbot. It is the combination of legal content, provenance, search, citator quality, historical law, workflow, document analysis, verification, and trust.

## Current strengths

NextLaw607 already has a meaningful brownfield foundation:

- NY-focused authority retrieval and source registry.
- CourtListener and New York Open Legislation integration.
- CitationFirewall and fail-closed authority promotion.
- Verified authority bank and temporal/provenance controls.
- Matter intake, research, drafting, adversarial critic, and workflow primitives.
- Criminal-defense workflow and skill infrastructure.
- Supabase/pgvector retrieval with strict server-side isolation.
- ContinuityOS routing, memory, checkpoints, deterministic gates, evals, and release controls.
- PWA/offline and authentication/entitlement foundations.

## Main parity gaps

1. Corpus breadth, depth, historical coverage, and measurable completeness.
2. Citator graph depth and treatment classification comparable in usefulness to KeyCite/Shepard's.
3. Classic legal search: Boolean/terms-connectors, citation lookup, filters, search-within, result controls.
4. Secondary sources and practical guidance.
5. Dockets, filings, procedural intelligence, and analytics.
6. Large-scale matter/document analysis.
7. Secure matter knowledge management and collaboration.
8. Enterprise governance, integrations, reliability, editorial operations, and support.

## Product requirements

### Authoritative legal corpus

Build a source-controlled, versioned legal corpus with measurable coverage. New York first:

- Court of Appeals.
- Appellate Division by Department.
- Relevant New York trial-level opinions where available.
- New York statutes, court rules, and regulations.
- Historical versions where legally material.
- U.S. Supreme Court, Second Circuit, and relevant federal district sources.
- Source class, jurisdiction, court, date, citation, version/effective range, URL, content hash, parser version, ingestion state, and verification timestamps.
- Coverage manifest and completeness metrics by source/jurisdiction/date range.

### Search and retrieval

Support both traditional legal search and AI-assisted research:

- Natural-language search.
- Boolean/terms-and-connectors.
- Citation and party-name lookup.
- Jurisdiction, court, date, source, document type, and precedential-status filters.
- Search within results.
- Related/citing/cited authority.
- Saved searches, folders, history, pinning, and comparison.
- Hybrid lexical + vector + metadata ranking.
- Citation-graph expansion.
- Transparent ranking/provenance metadata.
- Retrieval results remain candidates until verified.

### Citator

Develop a NextLaw citator that provides:

- Citing references.
- Subsequent history.
- Treatment classes such as followed, distinguished, limited, questioned, criticized, overruled/superseded where supported.
- Statutory amendment/version history.
- Court/jurisdiction/depth-of-discussion filters.
- Alerts and citation-drift detection.
- Human-review queue for ambiguous treatment.
- Evidence links supporting every treatment signal.
- Benchmark sets for treatment accuracy and negative-authority recall.

### Deep Research

A research job should:

1. Parse the question and jurisdiction.
2. Identify assumptions and missing facts.
3. Build issue/subissue tree.
4. Search controlling primary authority.
5. Search relevant persuasive and secondary material.
6. Search adverse/contrary authority.
7. Reconcile temporal and procedural posture.
8. Verify citations and authority status.
9. Synthesize rules and factual distinctions.
10. Produce a cited answer, research log, contrary-authority section, and unresolved gaps.

### Drafting and verification

Support motions, briefs, memoranda, affirmations/declarations, suppression papers, discovery papers, letters, sentencing/mitigation material, and related litigation documents.

Requirements:

- Draft from matter facts, verified research, approved templates, and user instructions.
- Proposition-to-authority mapping.
- Fact-to-record mapping.
- Quote/pinpoint verification.
- Citation formatting and table-of-authorities support.
- Adversarial counterargument pass.
- Missing-authority and unsupported-assertion detection.
- Version history, redline/revision, reviewer approval.
- Never label a draft review-ready while required citation/quotation checks are unresolved.

### Secure Matter Workspace

A matter must contain isolated, permissioned:

- Documents and OCR/extraction output.
- Facts, entities, chronology, and issue map.
- Research, pinned authorities, notes, drafts, deadlines, appearances, and work product.
- Matter-level AI history/checkpoints.
- Export/delete/retention controls.
- Audit trail.
- Encrypted/local-offline cache with explicit staleness and scope.

### Document analysis

Provide source-traceable analysis across tens, then hundreds, then thousands of documents:

- Batch summaries.
- Question matrix / tabular analysis.
- Structured extraction schemas.
- Contradiction and missing-document detection.
- Chronology.
- Deposition/hearing preparation.
- Discovery review.
- Evidence matrix.
- Contract/clause comparison only where in scope.
- Every extracted answer must link to document/page/span.

### Practical guidance

Build an original, source-linked New York criminal practical-guidance layer:

- Issue notes.
- Checklists.
- Motion/hearing workflows.
- Filing/service requirements.
- Procedural timelines.
- Discovery workflows.
- Client intake and mitigation checklists.
- Court/county practice notes where verified.
- Forms/templates linked to controlling primary authority.

### Dockets, procedure, and analytics

- Docket/event ingestion where legally and technically available.
- Filing and appearance timeline.
- Deadline calculator with rule/version provenance and explicit assumptions.
- Judge/court public-ruling statistics with sample/coverage disclosure.
- Motion/outcome/time-to-disposition analytics.
- No speculative personal profiling or unsupported behavioral claims.

### Firm knowledge and collaboration

- Permissioned prior briefs, motions, memos, templates, and playbooks.
- Search and retrieval across firm knowledge.
- Provenance, versioning, duplicate detection, and quality status.
- Roles, reviewers, comments, approvals, activity/audit trail.
- Matter/research/draft handoff.

### Security and AI model layer

- Strong authentication and role-based/matter-scoped authorization.
- Encryption in transit/at rest.
- Provider and retention disclosures.
- Secrets management.
- Privacy-safe telemetry.
- Model/provider routing by privacy, capability, latency, and cost.
- No silent provider substitution that violates declared constraints.
- Deterministic/local paths before model calls where possible.
- Reproducible agent/tool logs without leaking privileged matter text.

## Flagship NY criminal vertical

The deepest end-to-end experience should cover:

- Encounter/arrest and constitutional interaction.
- Charge elements.
- Suppression.
- Statements/Huntley.
- Identification procedures.
- Discovery/CPL Article 245.
- Brady/Giglio issue tracking.
- CPL 30.30.
- Bail/pretrial.
- Grand jury/indictment.
- Plea/sentencing/mitigation.
- Trial/evidence.
- Preservation/direct appeal.
- CPL 440 and related collateral issues.
- Probation/restitution.
- Record/transcript provenance.

## Non-goals

- Claiming NextLaw has Westlaw/Lexis proprietary editorial content or identical corpus rights.
- Treating RAG output as legal authority.
- Filing papers automatically without an explicit, separately authorized workflow.
- Expanding every legal practice area before the NY-criminal research/citator core is dependable.
- Hiding corpus gaps, stale sources, unresolved citator uncertainty, or verification failures.

## Success metrics

Research:
- Controlling-authority recall.
- Adverse-authority recall.
- Citation validity.
- Treatment accuracy.
- Stale-law detection.
- Unsupported-assertion rate.
- Time to research completion.

Drafting:
- Citation/quote verification rate.
- Missing-authority rate.
- Adversarial issue coverage.
- Attorney edit distance/time saved.

Document analysis:
- Extraction accuracy.
- Source-span traceability.
- Contradiction/chronology accuracy.
- Throughput and failure rate.

Platform:
- Matter isolation failures = zero in release gates.
- Source provenance coverage.
- Search latency.
- Cost per task.
- Repeat usage and completion rate.
- Trust incidents.

## Definition of functional comparability

For a declared scope, NextLaw607 may call itself functionally comparable only when:

- Attorneys can perform classic search without chat.
- Deep Research produces inspectable, source-backed results.
- Corpus coverage is measured and disclosed.
- Citator performance is benchmarked.
- Every cited authority resolves to source evidence.
- Adverse-authority search is mandatory for research-complete status.
- Matter/document analysis is source-traceable.
- Drafting is record- and authority-grounded with adversarial review.
- Historical/freshness metadata is available.
- Matter isolation, privacy, and security gates pass.
- Scope claims clearly identify what is and is not covered.
