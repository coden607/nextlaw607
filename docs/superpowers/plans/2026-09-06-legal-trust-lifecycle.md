# Legal Trust + Criminal Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:verification-before-completion. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen NextLaw607 so citation-history evidence is purpose-validated and criminal-procedure deadlines are surfaced only from classified, traceable sources.

**Architecture:** Extend the source registry with explicit source capabilities rather than treating every registered host as suitable for every verification task. Extend criminal-case state with typed deadlines that remain fail-closed unless their provenance is classified as court, docket, counsel, or verified statutory/rule authority. Keep all behavior deterministic and local; no network result is silently treated as verified law.

**Tech Stack:** Python 3.11+, dataclasses, pytest, existing NextLaw607 release gates.

**Spec:** Existing `src/nextlaw607/authority.py`, `src/nextlaw607/sources.py`, and `src/nextlaw607/procedure.py` contracts plus the branch's fail-closed release policy.

## Global Constraints

- Never force-update `main`; work only on `feat/legal-core-ts-pwa`.
- A source being registered does not make it suitable for citation-history analysis.
- Court dates and legal deadlines must not be invented from generic lifecycle knowledge.
- Repository copies may support research, but primary text verification remains separately required.
- Release remains incomplete unless all fail-closed release and browser evidence gates pass on the exact head revision.

---

### Task 1: Purpose-aware source trust

**Files:**
- Modify: `tests/test_legal_core.py`
- Modify: `src/nextlaw607/sources.py`
- Modify: `src/nextlaw607/authority.py`

**Interfaces:**
- Produces: `SourceCapability`, `SourceRegistry.supports(url, capability, jurisdiction=None)`.
- Citation firewall consumes `CITATION_HISTORY` capability for every history source and `PRIMARY_TEXT` for official-text cross-checks.

- [ ] **Step 1: Write failing tests** proving a statutes-only source cannot satisfy citation history, CourtListener can satisfy research-history evidence, and official court sources can satisfy primary-text verification.
- [ ] **Step 2: Run CI and verify RED** because `SourceCapability`/`supports` do not yet exist.
- [ ] **Step 3: Implement minimal capability metadata and firewall checks.**
- [ ] **Step 4: Run the full Python/web/release suite and verify GREEN.**
- [ ] **Step 5: Commit without modifying `main`.**

### Task 2: Provenance-bound criminal deadlines

**Files:**
- Modify: `tests/test_legal_core.py`
- Modify: `src/nextlaw607/procedure.py`

**Interfaces:**
- Produces: `DeadlineKind`, `CaseDeadline`, `CriminalCaseState.add_deadline(...)`, and deadline-aware `next_actions()` output.
- A deadline is displayable only when its source kind is one of `court_notice`, `docket`, `counsel_confirmation`, `statute`, or `court_rule`; otherwise insertion fails.

- [ ] **Step 1: Write failing tests** for trusted deadline insertion, unclassified-source rejection, chronological sorting, and source text in surfaced actions.
- [ ] **Step 2: Run CI and verify RED.**
- [ ] **Step 3: Implement the minimal deadline model.**
- [ ] **Step 4: Run the complete clean-checkout verification and browser evidence workflow.**
- [ ] **Step 5: Commit and preserve a fresh recovery artifact for the exact verified head.**

### Task 3: Release evidence

**Files:**
- Verify: `.github/workflows/ci.yml`
- Verify: `.github/workflows/browser-release-evidence.yml`
- Verify: `src/nextlaw607/release_checks.py`

**Interfaces:**
- Consumes exact Git commit SHA.
- Produces CI/browser evidence tied to that revision.

- [ ] **Step 1: Confirm CI checks run on the final head.**
- [ ] **Step 2: Confirm browser accessibility, E2E, PWA/offline, console/network, and performance gates run on the exact head.**
- [ ] **Step 3: Leave release status blocked if any required evidence is missing or stale.**
