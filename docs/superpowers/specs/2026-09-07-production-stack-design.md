# NextLaw607 2026 Production Stack Design

## Goal
Build NextLaw607 into a production legal-intelligence PWA using the strongest applicable 2026 agent/RAG/security stack while preserving deterministic legal trust, privacy, fail-closed authorization, and exact-revision release evidence.

## Non-negotiable boundaries
- The existing CitationFirewall remains authoritative for legal-source trust; no LLM, RAG framework, memory layer, workflow engine, or evaluator may bypass it.
- Python stays behind the FastAPI boundary; the client remains TypeScript/PWA-first.
- Secrets never ship to the client or Git. `.env` values are local only; production secrets live in deployment/CI secret stores.
- User memory, case evidence, agent memory, and temporary chat context are separate namespaces. Memory is never legal evidence.
- External integrations fail closed when unavailable or misconfigured.
- No release is complete unless deterministic tests, security/privacy/legal evals, and exact-revision browser evidence all pass.

## Required production layers

### Application
React + Vite + TypeScript + Tailwind + shadcn/ui PWA; FastAPI service boundary; offline-safe rights/case workflows.

### Agent orchestration
Pydantic AI for typed model/agent boundaries; LangGraph for deterministic stateful workflows; Archon as a development/harness layer where it improves agent engineering; n8n for external/business automation only, never legal-trust decisions.

### Retrieval and knowledge
Docling for document/PDF parsing and structure-aware ingestion; Crawl4AI for permitted web ingestion; Supabase/Postgres as authoritative relational storage; pgvector for vector retrieval; Neo4j + Graphiti only for graph relationships that measurably improve legal research; Redis/Valkey only for queues/cache where justified.

### Memory
Mem0 for long-term assistant/user memory with explicit namespaces and consent/deletion controls. Memory output is untrusted context until independently verified when used in legal workflows.

### Safety and tool authorization
NeMo Guardrails for model/input/output/tool rails; deterministic NextLaw policy rails; explicit tool authorization (Arcade or equivalent) for sensitive external actions; Cloudflare edge controls for WAF/rate limiting/security headers/DDoS protection.

### Legal verification
Official-source-first retrieval; CourtListener as candidate research; CitationFirewall; jurisdiction/court hierarchy; temporal verification; citation-history independence; provenance; current-law checks; explicit uncertainty. Independent Claude evaluation may review outputs but cannot override deterministic legal gates.

### Evaluation and debugging
Pytest; TypeScript tests; Playwright E2E; Ragas for RAG quality; adversarial legal evals; Claude independent evaluator; accessibility/PWA/offline/Core Web Vitals gates. OpenTelemetry provides end-to-end traces; Langfuse provides LLM/agent traces/evals; Sentry provides runtime exception/performance diagnostics.

### Backend and commercial services
Supabase Postgres/Auth/RLS/Storage/pgvector/entitlements; Stripe for billing where applicable. Founder/non-billing grants remain server-authoritative and cannot be synthesized from client metadata.

### Delivery
Docker; GitHub Actions; Cloudflare deployment; dependency/secret/static scans; CodeRabbit-style supplemental review. Promotion is revision-bound and must rerun all applicable gates after every merge/tag/new exact revision.

## Integration policy
A tool is not marked implemented merely because its dependency is installed. `implemented` means it is wired into a real flow, secured, tested, included in CI, and documented. `configured` requires non-secret configuration plus declared secret names. `verified` requires exact-revision evidence.

Optional infrastructure such as Neo4j/Graphiti and Redis/Valkey remains required-to-evaluate rather than blindly required-to-run; it becomes a production dependency only after a measurable benefit and security/operability review.

## Initial implementation order
1. Authoritative Supabase entitlements schema/repository + RLS/security tests.
2. Machine-readable stack manifest and CI validator so required stack coverage cannot silently regress.
3. Structured ingestion boundary (Docling/Crawl4AI) feeding untrusted candidates into CitationFirewall.
4. Pydantic AI + LangGraph orchestration with explicit legal/tool boundaries.
5. Mem0 namespaces/consent/deletion and evidence-isolation tests.
6. NeMo/tool authorization and prompt-injection/tool-call tests.
7. OpenTelemetry + Langfuse + Sentry observability with privacy redaction.
8. Ragas + Claude independent evaluation lane.
9. Cloudflare/security/deployment hardening and final browser/device verification.
