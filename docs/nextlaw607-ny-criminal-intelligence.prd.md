# NextLaw607 — New York Criminal Intelligence PRD

**Status:** Proposed product intent  
**Scope:** New York criminal-law vertical first; architecture remains jurisdiction-extensible  
**Platform direction:** NextLaw607 is a legal application/pack on Continuity OS, not a second orchestration platform.

## 1. Problem Statement

People working with New York criminal matters must reconstruct the governing law, procedural posture, record, deadlines, evidence, controlling authority, adverse authority, and available remedies across fragmented sources. General-purpose AI can accelerate this work but can also produce unsupported propositions, stale law, invented citations, jurisdictional mistakes, and answers that ignore procedural posture.

NextLaw607 should make a New York criminal matter researchable as a verified, source-grounded system: retrieve the right law and record, show provenance, analyze the issue through adversarial legal lenses, and refuse to present an unsupported authority as verified.

The first serious vertical is **New York criminal law**. Nationwide coverage is explicitly deferred until the NY vertical demonstrates trustworthy end-to-end performance.

## 2. Evidence

Current repository evidence:
- NextLaw607 already implements a New York-oriented counsel terminal, authority harvesting, a Planner/Executor/Critic pattern, matter files, CourtListener/NY legislative retrieval, and a zero-hallucination rule.
- The repository already declares Continuity OS universal directives and canonical coden607 skills.
- Continuity OS Base already contains hybrid semantic RAG, Archon multi-agent orchestration, Jev routing, token optimization, guardrails, second-brain memory, and a PRD-to-PR software factory.
- The canonical skills repository already contains Legal War Room and NY criminal live-court/post-judgment procedures.

User/product evidence:
- The intended differentiator is not generic legal chat. It is a rigorous legal workbench capable of record-aware, jurisdiction-aware, citation-verified and adversarial analysis.
- The product should reuse Continuity OS and canonical skills rather than rebuilding orchestration independently in NextLaw607.

**Assumptions requiring validation:** legal professionals/pro se users will prefer a NY-specialized verified workflow over a broader but less transparent assistant; sufficient primary-law and case metadata can be obtained/licensed for the intended feature set; automated treatment classification can reach acceptable precision with human-verifiable evidence.

## 3. Thesis

Win narrowly before expanding broadly. A deeply indexed New York criminal system can be more useful for its target workflow than attempting to reproduce the nationwide breadth of Westlaw or Lexis at launch.

NextLaw607 should compete on:
1. source-grounded answers with visible provenance;
2. procedural-posture and record awareness;
3. temporal law — what governed on the relevant date;
4. adversarial analysis rather than one-sided drafting;
5. verified citation/treatment checks;
6. integrated matter, evidence, timeline and motion workflows;
7. low-cost agent orchestration through Continuity OS, Jev and token-saving skills.

## 4. Hypothesis

We believe combining a verified NY criminal corpus with record-aware hybrid retrieval, citation validation, temporal authority, and Legal War Room adversarial passes will let users reach a defensible research/drafting result faster and with fewer unsupported legal propositions than a generic AI workflow.

**RIGHT:** on a representative holdout suite of NY criminal research and drafting tasks, the system consistently retrieves controlling authority, exposes adverse authority, provides source provenance, and produces no fabricated citations while materially reducing manual research steps.

**WRONG:** the system regularly misses controlling/adverse authority, cannot reliably distinguish current from historical law, produces unsupported legal propositions, or requires enough manual verification that the integrated workflow provides no meaningful advantage.

Exact production thresholds are **TBD — needs validation** through a legal evaluation suite.

## 5. Target Users & JTBD

### Primary initial users
- New York criminal defense attorneys and supervised legal staff.
- Pro se litigants/researchers who need transparent primary sources and procedural organization.

### Secondary analysis lenses
These are analytical roles, not impersonation/persona claims:
- citizen/defendant;
- private security/complainant;
- responding officer;
- investigator/detective;
- prosecutor/ADA;
- defense counsel;
- court clerk/paralegal;
- trial judge;
- appellate counsel;
- appellate judge/panel;
- Attorney General/state appellate advocate;
- post-conviction reviewer.

### JTBD
When I am researching or preparing a New York criminal matter, I want the system to organize the record, retrieve the governing authority and contrary authority, show exactly what supports each proposition, and pressure-test the result from the relevant opposing/judicial perspectives so I can identify defects before relying on or filing the work.

### Non-users for Phase 1
- nationwide general-practice researchers;
- users seeking autonomous court filing or representation;
- non-NY criminal jurisdictions;
- civil/commercial practice except existing NextLaw features preserved during migration.

## 6. MVP

The thinnest end-to-end proof is one NY criminal matter workspace that can:

1. ingest a user-selected record/document set;
2. identify procedural posture and material issues;
3. retrieve relevant current/historical NY statutes and controlling/persuasive cases;
4. combine lexical and semantic retrieval with jurisdiction/date/court filtering;
5. attach provenance to every retrieved authority and record fact;
6. build a chronology and authority/citation graph;
7. run Legal War Room counsel → opponent/prosecutor → judge → appellate passes;
8. run a prove-me-wrong/adverse-authority search;
9. block or mark unsupported citations/propositions through CitationFirewall;
10. produce a research memo or draft with source-linked propositions and an unresolved-issues list.

A full Westlaw/Lexis replacement is not the MVP.

## 7. Required Product Capabilities

### NY criminal corpus
Coverage target:
- New York Constitution where relevant;
- Penal Law;
- Criminal Procedure Law;
- applicable court rules;
- NY Court of Appeals;
- Appellate Division Departments 1–4 with department metadata;
- relevant NY trial decisions where available;
- U.S. Supreme Court and Second Circuit for applicable federal questions;
- historical statutory versions/effective dates;
- later-citing/treatment metadata.

### Matter intelligence
- matter/case workspace;
- parties and caption;
- procedural posture;
- charges/counts and element mapping;
- record/evidence ledger with provenance;
- witness ledger;
- chronology/deadline ledger;
- issue/remedy map;
- preservation ledger;
- authority matrix;
- generated work product with claim-to-source traceability.

### Retrieval and RAG behavior
Product requirement, independent of implementation:
- retrieve by meaning and exact legal terminology;
- filter by jurisdiction, court hierarchy, department, date, document type and authority status;
- preserve paragraph/page/section-level source locations where available;
- distinguish record facts from public legal authority;
- support current-law and law-as-of-date queries;
- expose why a source was retrieved;
- permit direct inspection of the underlying authority.

### CitationFirewall
A legal proposition presented as verified must trace to a retrieved source that actually supports it. The system must:
- reject invented/unretrieved citations;
- distinguish holding, dicta, party argument and dissent where metadata/content permits;
- distinguish controlling from persuasive authority;
- flag unknown treatment rather than infer validity;
- verify quotations against retrieved source text;
- mark unresolved authority as [AUTHORITY NEEDED] or equivalent;
- retain source and retrieval provenance for audit.

### Citator/treatment capability
Long-term product requirement:
- cited-by graph;
- later history;
- positive/neutral/negative treatment evidence;
- followed/distinguished/limited/criticized/overruled/superseded concepts;
- treatment excerpts linked to the later opinion;
- no treatment label without inspectable evidence;
- human correction/feedback path.

### Criminal workflow modules
- intake/procedural posture;
- offense elements;
- arrest/search/seizure;
- statements/interrogation;
- suppression;
- discovery/CPL article 245;
- Brady/Giglio;
- confrontation/hearsay/evidence;
- Sandoval/Molineux/Ventimiglia;
- speedy trial;
- bail;
- plea/sentencing;
- probation/VOP;
- restitution;
- trial preservation;
- direct appeal;
- CPL 330/410/440/450/460;
- ineffective assistance;
- post-judgment record vs outside-record analysis.

## 8. Continuity OS Product Requirement

NextLaw607 must consume Continuity OS capabilities instead of duplicating them where practical.

Always-on operating behavior:
- **compress-token-spend** — search/retrieve narrowly before loading large context; cheapest capable tier; cache-friendly stable prefixes; concise outputs; sampling rather than wasteful universal grading where appropriate.
- **route-with-jev** — repeated classification/routing/guardrail decisions use Jev/deterministic gates before expensive model calls.
- **route-interrupts** — preserve active work across user steering.
- **maintain-second-brain** — durable project state vs dated events.
- **isolate-agent-runs** — gate destructive/irreversible operations and isolate autonomous work.
- **enforce-with-hooks** — deterministic/event-time enforcement for invariants that cannot rely on prompts.
- **run-software-factory** — PRD → architecture → slices → implementation → validation → PR with explicit autonomy.
- **anticipate** — surface high-value next actions without silently performing destructive/external actions.

Canonical skill source: **coden607/skills**. NextLaw607 should reference/sync canonical skills rather than maintain divergent copies.

## 9. Legal Skill Program

Existing Legal War Room remains the master legal-analysis workflow.

New composable skills should be created only where they add reusable deterministic workflow, including:
- ny-criminal-intake
- ny-criminal-issue-spotter
- ny-penal-law-elements
- ny-cpl-procedure
- ny-criminal-discovery
- ny-search-seizure
- ny-interrogation-statements
- ny-evidence
- ny-suppression
- ny-speedy-trial
- ny-bail
- ny-plea-sentencing
- ny-probation-vop
- ny-restitution
- ny-appellate-review
- ny-cpl-440
- ny-ineffective-assistance
- legal-citation-validator
- legal-adverse-authority
- legal-citator
- legal-record-auditor
- legal-transcript-auditor
- legal-evidence-auditor
- legal-preservation-auditor
- legal-timeline-builder

Role/lens skills should remain source-constrained:
- role-citizen
- role-security
- role-police
- role-investigator
- role-prosecutor
- role-defense
- role-trial-judge
- role-appellate-counsel
- role-appellate-judge
- role-attorney-general

Roles do not get separate facts. They consume the same verified record and authority set and identify different issues, arguments, burdens and failure modes.

## 10. MCP / Connector Requirements

The product should expose a common research/tool boundary so legal workflows are not hard-wired to one provider.

Initial integrations should support:
- CourtListener / Free Law Project for available opinions/citation data;
- official New York legislative sources for statutes and amendments;
- repository/project tools for engineering workflows;
- document/file ingestion for matter records;
- future licensed/commercial legal sources through adapters without changing the legal workflow contract.

Connector output must be normalized into a common authority/provenance representation before Legal War Room or CitationFirewall treats it as verified.

## 11. Success Metrics

Initial metrics, with final thresholds **TBD — needs validation**:
- fabricated citation rate on holdout suite: target 0;
- unsupported verified-proposition rate: target 0;
- controlling-authority recall: threshold TBD;
- adverse-authority recall: threshold TBD;
- historical-law/date correctness: threshold TBD;
- citation/source traceability: 100% for verified propositions;
- retrieval precision at top-k: threshold TBD;
- end-to-end task completion time vs baseline manual/generic-AI workflow: improve materially, threshold TBD;
- cost per completed research workflow: measured and budgeted by task class;
- regression suite pass rate across canonical NY criminal scenarios: threshold TBD.

## 12. Non-goals

Phase 1 will not:
- reproduce nationwide Westlaw/Lexis breadth;
- promise exhaustive coverage where source licensing/access does not support it;
- autonomously file court papers;
- impersonate attorneys, judges, prosecutors, police, or officials;
- hide uncertainty or fabricate missing treatment;
- treat an LLM summary/headnote as the opinion's holding without source verification;
- rebuild Continuity OS orchestration inside NextLaw607;
- allow role lenses to mutate the underlying factual record.

## 13. Product Phases

### Phase A — Foundation/migration
Prove which current NextLaw components should be kept, ported or replaced by Continuity OS Base capabilities. Preserve useful product behavior and remove duplicate infrastructure.

### Phase B — NY criminal MVP
Verified corpus + matter workspace + hybrid retrieval + CitationFirewall + Legal War Room + one complete research/drafting flow.

### Phase C — Citator and temporal intelligence
Citation graph, later-history/treatment evidence, historical statutes, stronger adverse-authority retrieval and evaluation.

### Phase D — Criminal workflow depth
Specialized modules and role lenses, evidence/transcript/preservation workflows, sentencing/post-conviction depth.

### Phase E — NY breadth
Extend the same verified architecture into additional New York practice areas.

### Phase F — jurisdiction expansion
Second Circuit/federal depth and then additional states only after measurable NY quality gates are met.

## 14. Acceptance / Evaluation Program

A release candidate must be tested against a versioned holdout set containing:
- straightforward and ambiguous statute questions;
- controlling vs persuasive authority;
- conflicting Appellate Division authority;
- superseded/amended statutory text;
- adverse authority;
- false citation traps;
- fact/record contradictions;
- procedural posture traps;
- preservation and standard-of-review questions;
- mixed state/federal constitutional issues;
- CPL Article 245 and suppression scenarios;
- sentencing/probation/restitution/post-judgment scenarios.

Each evaluation records retrieved sources, final authorities, missed authority, unsupported claims, model/tool route, token/cost telemetry, latency and human-verification result.

## 15. Open Questions

- [ ] Which source set is legally/licensing-wise sufficient for production-grade NY opinion coverage?
- [ ] What minimum citator treatment accuracy is required before treatment labels are shown without a warning?
- [ ] What holdout corpus and expert review process will establish controlling/adverse-authority recall?
- [ ] Which existing NextLaw components are keep/port/replace after the migration inventory?
- [ ] Which Continuity OS Base modules are stable enough to consume directly versus through adapters?
- [ ] What is the product's first paid/production user segment: defense counsel, supervised staff, pro se research, or another segment?
- [ ] Which historical statute/version source will be canonical?
- [ ] Which matter data requires encryption, retention controls, or local-only operation in production?
- [ ] What commercial data integrations, if any, are needed after the open-source/public-source MVP?
- [ ] What exact quality thresholds graduate NY Criminal from beta?

## 16. Decision

Proceed with **New York criminal law as the first deep vertical**, built as a NextLaw607 application/pack on top of Continuity OS capabilities and canonical coden607 skills. Validate the end-to-end legal research loop before expanding jurisdictional breadth.
