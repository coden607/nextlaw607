# NextLaw607

New York criminal-law research and drafting terminal. It is intentionally restricted to criminal law and criminal procedure.

Not a law firm. Not legal advice. A human New York attorney must review anything before execution or filing.

## What it does

- **Criminal instrument desk** — suppression, discovery, speedy-trial, sentencing, appellate, and post-conviction work products tied to verified criminal-law authority.
- **Authority harvest** — CourtListener v4 opinions (NY / Appellate Division / Supreme / 2d Cir.) plus NY Senate Open Legislation pulls and a verified internal bank the critic is allowed to trust.
- **Planner · Executor · Critic triad** — one user-initiated Grok run. Score below 85 forces rewrite. Unverified cites are rejected.
- **Matter files** — local intake, captions, counties, parties. Nothing is a court filing.
- **Playbook** — persona, skills, MCP gateway, and the six-step workflow.
- **Stack** — Cole Medin’s 2026 AI-first stack mapped onto this counsel terminal.

Default scope: New York criminal law and criminal procedure only. Federal constitutional criminal authority is included where it governs New York criminal proceedings. Hierarchy is Court of Appeals → the relevant Appellate Division → other departments (persuasive) → trial courts, with SCOTUS/Second Circuit authority applied where controlling.

## Zero-hallucination rule

The model may cite only:

1. The verified statute/case bank in `src/lib/corpus.ts`
2. Live CourtListener / NY Senate hits from the current run

Anything else is marked `[AUTHORITY NEEDED]` or `[UNVERIFIED]` and the critic fails the draft.

## Local development

```bash
npm install
npm run dev
```

Server-only environment (never `VITE_`):

| Variable | Purpose |
| --- | --- |
| `XAI_API_KEY` | Grok counsel + optional TTS |
| `COURTLISTENER_API_TOKEN` | Raises Free Law Project rate limits |

Without a model key the desk still fills verified criminal-law templates offline.

```bash
npm run typecheck
npm run build
```

## ContinuityOS

This repo is also the first legal-intelligence pack on ContinuityOS (`coden607/continuityos`).

```bash
continuity config-check continuity.toml
continuity execute "Explain the task" --config continuity.toml
```

Pack metadata lives in `packs/nextlaw607/`.

## Disclaimer

Output is a criminal-law research and drafting aid. A licensed attorney should review work before filing or relying on it. The terminal will not pretend a PDF is filed.


## NY Criminal / Continuity OS roadmap

The first deep legal-intelligence vertical is New York criminal law, implemented as a NextLaw607 application/pack on Continuity OS rather than a duplicate orchestration stack.

- [Product requirements](docs/nextlaw607-ny-criminal-intelligence.prd.md)
- [Architecture and migration decision](docs/nextlaw607-ny-criminal-continuity-architecture.md)

Implementation starts with a keep/port/replace/retire inventory of the existing NextLaw code. Preserve useful product behavior; replace shared infrastructure only after parity is demonstrated. Canonical cross-agent skills remain in `coden607/skills`, with `compress-token-spend`, Jev routing, Software Factory and Legal War Room forming the default workflow.


### Agent/runtime enforcement

The Continuity route is machine-checked, not memory-dependent. Run `sh scripts/continuity-preflight.sh`; pull requests also run the `continuity-contract` CI check. See [Continuity enforcement contract](docs/nextlaw607-continuity-enforcement.md).
