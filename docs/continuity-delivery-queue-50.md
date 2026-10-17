# Continuity OS delivery queue: next 20 + anticipated 30

Applies Software Factory, Jev-first routing, token compression, isolation, second-brain, hooks, and Legal War Room. Items are not shipped until acceptance gates pass.

## Next 20 — committed sequence

1. Continuity runtime adapter — typed boundary; fail closed; never promotes legal authority.
2. Jev deterministic router — routine routing/guardrail decisions before model calls; deterministic fallback.
3. Token budget policy — task-class budgets, cheapest-capable tier, context caps, escalation reasons.
4. Routing decision ledger — privacy-safe route/cost/latency metadata; no prompts, facts, secrets, or privileged text.
5. Continuity health gate — explicit unavailable/degraded/ready states and tested safe fallback.
6. Agent-run isolation — per-run namespace/checkpoint IDs; prohibit cross-run leakage.
7. Matter-scoped second brain — user/matter namespaces; deny cross-matter reads by default.
8. Interrupt checkpointing — resumable task checkpoints compatible with route-interrupts.
9. Software Factory task envelope — PRD → architecture → implementation → test → review → verify state machine.
10. Hook enforcement layer — pre-model, pre-tool, post-tool, and stop hooks for mandatory invariants.
11. Legal skill registry — canonical skill IDs/version metadata; no divergent embedded copies.
12. Legal War Room dispatcher — issue decomposition/adversarial passes through canonical legal skill.
13. NY criminal issue classifier — deterministic mapping to suppression/discovery/speedy-trial/bail/plea/sentencing/trial/appeal/440.
14. Authority hierarchy scorer — jurisdiction/court/department/precedential weight separate from semantic relevance.
15. Temporal-law filter — offense/proceeding/amendment/effective-date/retroactivity as retrieval constraints.
16. Hybrid retrieval fusion — BM25/FTS + pgvector + metadata filters with score provenance.
17. Citation graph expansion — cited/citing discovery remains candidate-only until CitationFirewall verification.
18. Adverse-authority pass — mandatory counter-authority search before research-complete.
19. Record-gap detector — identify missing facts/documents/transcript portions; never invent facts.
20. NY criminal benchmark v1 — retrieval, hierarchy, temporal correctness, citation support, adverse authority, fail-closed cases.

## Anticipated 30

21. Citator treatment classifier with explicit-vs-inferred labels and confidence.
22. Human-review queue for uncertain treatment/history.
23. Statute version graph and historical text snapshots.
24. Regulation/court-rule versioning.
25. Appellate Division department-aware controlling-authority resolver.
26. Federal/NY interaction resolver for constitutional issues.
27. Suppression workflow pack.
28. CPL Article 245 discovery workflow pack.
29. CPL 30.30 speedy-trial timeline engine.
30. Bail/pretrial workflow pack.
31. Grand-jury/indictment workflow pack.
32. Plea/sentencing exposure workflow pack.
33. Trial/evidence workflow pack.
34. Direct-appeal preservation workflow pack.
35. CPL 440 post-judgment workflow pack.
36. Probation/restitution workflow pack.
37. Transcript issue extractor tied to exact page/line provenance.
38. Evidence inventory and chain-of-custody gap auditor.
39. Preservation/harmless-error matrix.
40. Motion-outline generator restricted to verified authority and user facts.
41. Argument/counterargument table with burden and standard of review.
42. Authority table generator with source/status/last-verified metadata.
43. Research freshness scheduler that marks stale verification rather than silently trusting it.
44. Official-source reconciliation when discovery indexes disagree.
45. Duplicate/opinion-family resolver.
46. Citation-format normalizer with canonical IDs.
47. Query decomposition for multi-issue criminal matters.
48. Retrieval explanation panel: ranking factors without hidden model reasoning.
49. Matter-level audit export: provenance, gates, sources, uncertainty, verification dates.
50. Release-readiness dashboard driven only by machine evidence.

## Cross-cutting gates

- CitationFirewall is the sole promotion boundary into verified/citable legal authority.
- RAG, model output, memory, MCP, Archon, n8n, and Continuity routing remain candidate/advisory layers.
- Secrets and privileged/matter text never enter routing telemetry.
- Authorization and Supabase RLS remain server-enforced.
- Deterministic/Jev decisions precede expensive model calls when applicable.
- Model escalation records a machine-readable reason and budget class.
- Existing tests are extended, never bypassed or weakened.
- Exact-revision CI, security, privacy, legal, browser, and deployment gates remain fail-closed.
- No standalone Continuity component is retired until parity evidence exists.

## Delivery slices

Slice A (1–5): Continuity routing substrate.
Slice B (6–10): execution safety.
Slice C (11–15): legal control plane.
Slice D (16–20): research quality.

Items 21–50 remain anticipated backlog until evidence from the first four slices validates their dependencies.