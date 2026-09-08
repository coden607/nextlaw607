# NextLaw607 2026 Production Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate and verify the approved 2026 production AI/RAG/security stack without weakening NextLaw607's deterministic legal-trust boundaries.

**Architecture:** Keep the TypeScript PWA and FastAPI legal core separated. Add typed orchestration, ingestion, memory, guardrails, observability and production services behind explicit interfaces; all legal assertions still pass through CitationFirewall and all external failures fail closed.

**Tech Stack:** TypeScript/PWA, FastAPI, Supabase/Postgres/Auth/RLS/pgvector, Pydantic AI, LangGraph, Archon, n8n, Docling, Crawl4AI, Mem0, NeMo Guardrails, Arcade/equivalent tool authorization, Langfuse, OpenTelemetry, Sentry, Ragas, Playwright, Claude evaluator, Cloudflare, Docker, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-07-production-stack-design.md`

## Global Constraints
- Never force-update or overwrite `main`.
- CitationFirewall remains the final legal-source trust boundary.
- Memory and model outputs are never evidence by themselves.
- Secrets remain outside Git/client bundles.
- Add production behavior test-first; observe RED before GREEN.
- Every promoted revision reruns CI, legal/security/privacy evals, browser accessibility/performance/E2E/PWA, and deployment checks.

---

### Task 1: Authoritative Supabase entitlement backend
**Files:** create `src/nextlaw607/supabase_entitlements.py`, `supabase/migrations/202609070001_entitlements.sql`; modify `src/nextlaw607/access_config.py`, `.env.example`; test `tests/test_supabase_entitlements.py`, `tests/test_access_config.py`.

**Interfaces:** `SupabaseEntitlementRepository.lookup(subject: str) -> Mapping[str, Any] | None`; `entitlement_provider_from_environment()` injects this lookup into `RepositoryEntitlementProvider`.

- [x] Add failing tests proving server credentials perform an authoritative subject-filtered lookup, malformed/non-200 responses fail closed, and client metadata cannot grant access.
- [x] Run CI and confirm RED is caused by the missing repository.
- [x] Implement minimal HTTPS-only Supabase REST repository and wire it from environment.
- [x] Add schema/RLS migration: entitlement rows keyed to `auth.users`, deny direct client writes, service/server ownership for grants.
- [x] Add `SUPABASE_SECRET_KEY` to `.env.example` as server-only.
- [x] Rerun full verification and confirm GREEN.

### Task 2: Stack manifest and CI regression gate
**Files:** create `config/production-stack.json`, `src/nextlaw607/stack_contract.py`, `tests/test_stack_contract.py`; modify `scripts/verify.sh`.

**Interfaces:** manifest states `required|evaluate`, lifecycle `planned|implemented|configured|verified`, environment variable names, tests/evidence paths.

- [x] Write failing tests for omitted required components and invalid status transitions.
- [x] Observe RED.
- [x] Implement validator and baseline manifest covering every approved component.
- [x] Add validation to `verify.sh` and observe GREEN.

### Task 3: Ingestion boundary
**Files:** create `src/nextlaw607/ingestion/` adapters and tests.

- [x] RED tests: Docling/Crawl4AI outputs are untrusted candidates and cannot become verified authorities directly.
- [ ] Implement concrete Docling and Crawl4AI runtime adapters with provenance/content hashing and bounded inputs. The shared candidate boundary is implemented; external library bindings remain pending.
- [x] Route candidate legal material through CitationFirewall; verify GREEN.

### Task 4: Typed agent workflow
**Files:** create `src/nextlaw607/agents/` and workflow tests.

- [x] RED tests for typed state, deterministic legal verification node, tool allowlisting, and fail-closed transitions.
- [ ] Add concrete Pydantic AI agent boundary and LangGraph state machine. The deterministic typed orchestration core is implemented and verified; framework bindings remain pending.
- [ ] Keep Archon as development/harness integration, not per-request legal authority.
- [x] Verify model/tool failures never bypass legal verification in the deterministic orchestration core.

### Task 5: Mem0 memory isolation
**Files:** create memory adapter/config/tests.

- [ ] RED tests for separate user/case/agent/session namespaces, consent, delete/export, and prohibition on treating memory as authority.
- [ ] Implement Mem0 adapter with privacy redaction and explicit IDs.
- [ ] Verify isolation/deletion and fail-closed behavior.

### Task 6: NeMo and tool guardrails
**Files:** create guardrail configuration/adapters/tests.

- [ ] RED adversarial tests for prompt injection, unauthorized tool calls, PII leakage, and attempts to bypass CitationFirewall.
- [ ] Integrate NeMo rails plus deterministic tool authorization (Arcade or equivalent).
- [ ] Verify allowed flows continue and denied flows fail closed.

### Task 7: Observability/debugging
**Files:** create telemetry configuration and privacy tests.

- [ ] RED tests that secrets/tokens/legal private content are redacted from telemetry.
- [ ] Wire OpenTelemetry spans, Langfuse LLM/agent traces/evals, and Sentry exceptions/performance.
- [ ] Verify trace correlation without sensitive payload leakage.

### Task 8: Evaluation lane
**Files:** extend `evals/`, CI workflow and release validator.

- [ ] Add Ragas retrieval/answer-grounding cases and Claude independent-judge schema.
- [ ] Require deterministic checks to outrank any LLM judge result.
- [ ] Add adversarial legal/current-authority regression corpus.
- [ ] Publish exact-revision machine-readable evaluation evidence.

### Task 9: Web platform and production deployment
**Files:** PWA dependencies/components, Cloudflare config/workflows, security tests.

- [ ] Migrate/confirm React + Vite + Tailwind + shadcn/ui without breaking PWA/offline behavior.
- [ ] Add Cloudflare deployment bindings, WAF/rate-limit/security-header expectations and smoke checks.
- [ ] Add Stripe entitlement reconciliation where paid plans require it.
- [ ] Evaluate Redis/Valkey and Neo4j/Graphiti; activate only with measured benefit.
- [ ] Run clean-checkout CI, security/privacy/legal evals, browser E2E/accessibility/Core Web Vitals/offline/PWA and deployment smoke tests against the exact promotion revision.
