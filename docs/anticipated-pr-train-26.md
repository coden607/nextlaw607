# Anticipated delivery train: next 26 PRs

Dependency-ordered backlog for PRs following the current execution-safety slice. Each PR stays independently reviewable, preserves CitationFirewall/RLS/privacy gates, and uses deterministic/Jev routing before model spend when applicable.

1. Matter-scoped second-brain adapter — align MemoryScope and RunScope; deny cross-matter reads.
2. Interrupt/resume coordinator — checkpoint active phase and safely resume after steering.
3. Software Factory state machine — PRD → architecture → implement → test → review → verify.
4. Hook enforcement bus — pre-model/pre-tool/post-tool/stop invariant hooks.
5. Canonical skill registry — IDs, versions, required capabilities, provenance.
6. Legal War Room dispatcher — issue decomposition plus adversarial review stages.
7. NY criminal deterministic issue classifier — zero-token first pass.
8. Authority hierarchy scorer — jurisdiction, court, department, precedential weight.
9. Temporal-law constraint model — offense/proceeding/effective/amendment/retroactivity dates.
10. Hybrid retrieval fusion — lexical + vector + metadata with deterministic provenance.
11. Citation graph candidate expansion — citing/cited neighbors remain unverified candidates.
12. Adverse-authority search pass — required before research-complete status.
13. Record-gap detector — missing facts/documents/transcript portions without invention.
14. NY criminal benchmark v1 — gold cases and fail-closed assertions.
15. Citator treatment schema — explicit/inferred treatment, confidence, provenance.
16. Citator human-review queue — uncertain treatment cannot silently promote.
17. Statute historical-version graph — effective ranges and amendment lineage.
18. Court-rule/regulation versioning — historical 22 NYCRR/regulatory applicability.
19. Department-aware controlling-authority resolver — NY appellate hierarchy conflicts.
20. Federal/NY constitutional interaction resolver — controlling vs persuasive authority.
21. Suppression workflow pack — issue tree, burdens, verified-authority requirements.
22. CPL Article 245 discovery workflow pack — obligations, timing, record gaps.
23. CPL 30.30 timeline engine — event ledger and deterministic chargeable-time calculations.
24. Bail/pretrial workflow pack — statutory factors and procedural posture.
25. Grand-jury/indictment workflow pack — defects, preservation, procedural gates.
26. Plea/sentencing workflow pack — exposure ranges, prerequisites, verified inputs.

## Anticipated next 30 through Continuity OS

These are PRs 27–56 in dependency order. Each feature is assigned to a Continuity primitive so execution remains deterministic-first, resumable, isolated, and token-efficient.

27. Trial/evidence workflow pack — Legal War Room + canonical evidence skills; verified-source-only issue trees.
28. Direct-appeal preservation workflow — second brain + record auditor; map objections/rulings/standards to exact record provenance.
29. CPL 440 workflow pack — Legal War Room + timeline/record-gap gates; separate record and extra-record claims.
30. Probation/restitution workflow pack — deterministic eligibility/deadline calculations before synthesis.
31. Transcript provenance extractor — isolated parser run; page/line anchors become first-class evidence metadata.
32. Evidence inventory/gap auditor — deterministic inventory; missing-chain and missing-document flags before model analysis.
33. Preservation/harmless-error matrix — Jev classifies issue posture; premium synthesis only for supported appellate analysis.
34. Verified motion-outline generator — model receives only user facts plus CitationFirewall-approved authority.
35. Argument/counterargument matrix — Software Factory adversarial stage with burden/standard-of-review fields.
36. Authority-table generator — deterministic rendering of citation, court, date, status, source, verification timestamp.
37. Research freshness scheduler — second-brain state marks stale authorities and revalidation needs without silently refreshing trust.
38. Official-source reconciliation — deterministic conflict resolver when CourtListener/official sources disagree.
39. Opinion-family/dedup resolver — Jev/deterministic canonicalization before embedding or model use.
40. Citation normalizer — canonical case/statute/rule identifiers with no model call for standard formats.
41. Multi-issue query decomposer — Jev first-pass decomposition; escalate only ambiguous issue boundaries.
42. Retrieval explanation layer — expose ranking factors and provenance without hidden chain-of-thought.
43. Matter audit export — immutable provenance/gate/source/uncertainty manifest; no privileged text in routing telemetry.
44. Release-readiness dashboard — Software Factory consumes machine evidence only; no self-reported green state.
45. Source registry + ingestion contracts — authoritative URL/source class, jurisdiction, version, hash, and parser status.
46. Immutable raw-source snapshots — content hash/version lineage so downstream chunks are reproducible.
47. Docling ingestion adapter — isolated parsing with schema validation and failure quarantine.
48. Canonical legal-ID resolver — cases/statutes/rules get stable IDs before graph/vector indexing.
49. Passage-level quotation verifier — exact source-span validation before quotation can enter a draft.
50. Source-availability/fallback monitor — deterministic health state for official sources and approved mirrors.
51. Eval sampling/Jev judge gate — deterministic tests on every run; expensive model judges sampled only where needed.
52. Token/cost budget dashboard — aggregate privacy-safe routing ledger data by task class and model tier.
53. Provider failover policy — Continuity routing enforces privacy/cost/capability constraints before provider selection.
54. Local/offline research cache — exact-version cache keyed by canonical authority IDs and source hashes.
55. Deterministic dedupe/context compressor — collapse repeated authorities/passages before context assembly.
56. Golden-trace regression replay — replay sanitized deterministic route/retrieval decisions against new releases.

## Continuity execution policy for PRs 27–56

- Route every task through Continuity's preflight and canonical skill selection first.
- Use Jev/deterministic logic for classification, normalization, routing, dedupe, budgets, and guardrails before LLM spend.
- Use narrow retrieval and reusable verified context; do not repeatedly load the same matter corpus.
- Keep runs and checkpoints isolated by user/matter/agent/run scope.
- Use second-brain state for durable non-authoritative workflow state; never for legal verification.
- Apply pre-model, pre-tool, post-tool, and stop hooks.
- Escalate local/free → economical → premium only when capability gates require it.
- Record only privacy-safe route/cost/latency metadata; no prompts, case facts, secrets, or privileged text.
- CitationFirewall remains the sole authority-promotion boundary.
- Merge only exact tested revisions after all required security/privacy/legal/CI/browser gates succeed.

## Train rules

- One coherent risk boundary per PR; combine only tightly coupled code/tests.
- Prefer deterministic code over LLM calls; Jev before model routing.
- Use cheapest capable model tier and narrow retrieval; premium synthesis only after verified context exists.
- No prompts, matter facts, secrets, or privileged text in route/cost telemetry.
- CitationFirewall alone promotes citable authority.
- Memory/checkpoints/orchestration/model output remain non-authoritative.
- Never weaken existing CI to merge.
- Merge only exact tested head revision after all required checks succeed.
- Rebase/retest when a dependency PR changes a downstream assumption.
- Stop and redesign rather than accumulate compatibility shims around an unstable boundary.
