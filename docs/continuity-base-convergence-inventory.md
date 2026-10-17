# Continuity Base convergence inventory

Status: first brownfield inventory after PR #13. This document is an implementation gate, not a claim that the standalone Continuity runtime has already been replaced.

## Decision rule

- **KEEP** — NextLaw-specific behavior that remains authoritative.
- **PORT** — useful NextLaw behavior that should move behind a Continuity Base interface.
- **REPLACE** — generic infrastructure already owned by Continuity Base.
- **RETIRE** — duplicate path removed only after parity evidence.
- **SPIKE** — uncertainty must be resolved before migration.

## Inventory

| Area | Current NextLaw implementation | Disposition | Cutover condition |
| --- | --- | --- | --- |
| Citation trust | `src/nextlaw607/authority.py`, `research.py` | KEEP | CitationFirewall remains the final fail-closed legal trust boundary. |
| Legal retrieval | `retrieval.py`, pgvector, CourtListener/NY adapters | KEEP + PORT | Preserve authority/provenance semantics while routing generic retrieval orchestration through Continuity Base. |
| Legal corpus | `src/lib/corpus.ts` and ingestion boundary | KEEP | No generic RAG component may promote a candidate to verified authority. |
| Temporal/current-law verification | authority/research/source hierarchy | KEEP | Explicit effective-date and current-law tests before expansion. |
| Legal War Room / legal skills | canonical `coden607/skills` plus repo legal logic | KEEP | Canonical skill remains source; repo consumes rather than forks it. |
| Model routing | app/model adapters and agent framework bindings | REPLACE incrementally | Continuity/Jev routing demonstrates parity and preserves legal gates. |
| Token/cost routing | ad-hoc model selection | REPLACE | `compress-token-spend` + Jev deterministic-first policy is enforced and observable. |
| Agent orchestration | Pydantic AI/LangGraph/Archon boundary | PORT | Continuity owns generic orchestration; NextLaw retains legal workflow definitions. |
| Memory | `src/nextlaw607/memory.py`, Mem0 adapter | PORT | Matter isolation/privacy tests pass through Continuity memory interface. |
| Guardrails/tool auth | `guardrails.py`, NeMo/tool authorization | PORT | Continuity enforcement composes with, never bypasses, CitationFirewall. |
| Verification/evals | verify scripts, Ragas/evals, release checks | KEEP + PORT | Software Factory invokes existing exact-revision gates unchanged. |
| Interrupts/isolation | repo/agent conventions | REPLACE | Continuity `route-interrupts` and `isolate-agent-runs` become executable runtime gates. |
| Second brain | local repo state + agent memory conventions | REPLACE/PORT | Continuity state is scoped so privileged matter data cannot leak across matters. |
| CI enforcement | GitHub workflows + Continuity Contract | KEEP | Required checks remain fail-closed. |
| UI/auth/data access | React/PWA, Supabase identity/RLS | KEEP | No Continuity migration changes client auth or RLS semantics without dedicated proof. |
| Deployment | Vercel/Cloudflare/Docker/GitHub | KEEP | Deployment remains independent from legal authority trust. |

## First migration slice

The first executable slice is deliberately narrow:

1. Preserve CitationFirewall and existing legal retrieval behavior.
2. Add a Continuity-facing adapter boundary for generic routing/orchestration.
3. Route deterministic/zero-token decisions through Jev before model selection.
4. Keep model execution behind existing server boundaries.
5. Record routing decisions without privileged matter text.
6. Run existing Python, web, security, privacy, eval, E2E and browser gates.
7. Do not retire the standalone Continuity entrypoint until parity is demonstrated.

## Required skills for this slice

Always-on: `compress-token-spend`, `route-with-jev`, `route-interrupts`, `maintain-second-brain`, `isolate-agent-runs`, `enforce-with-hooks`, `run-software-factory`.

Domain: `legal-war-room` and the smallest applicable legal audit/research skills.

## Spikes before destructive cutover

1. **Runtime contract:** identify the stable Continuity Base executable/API contract that NextLaw can call in CI and on the VPS without coupling to a developer-only path.
2. **Routing parity:** prove Jev/deterministic routing cannot bypass server-only model, authorization, or legal-trust boundaries.
3. **Memory privacy:** prove second-brain/memory namespaces cannot cross matter/user boundaries.
4. **RAG parity:** prove generic Continuity retrieval does not alter authority ranking or verification status.
5. **Failure semantics:** prove Continuity unavailable/error states fail closed or fall back only to an explicitly safe existing path.

## Retirement gate

Standalone ConOS/Continuity dependencies may be retired only when all five spikes have evidence, existing release gates are green on the exact cutover revision, and no duplicate path can bypass CitationFirewall, authorization, privacy isolation, or required CI.
