# NextLaw607

New York General Counsel terminal. It drafts instruments, harvests binding authority, and then attacks its own work as opposing counsel.

Not a law firm. Not legal advice. A human New York attorney must review anything before execution or filing.

## What it does

- **Instrument desk** — NY-governed templates (ICA, NDA, parenting stipulation, settlement, residential lease, LLC operating agreement, criminal defense workup) with required statutes and Court of Appeals cases wired in.
- **Authority harvest** — CourtListener v4 opinions (NY / Appellate Division / Supreme / 2d Cir.) plus NY Senate Open Legislation pulls and a verified internal bank the critic is allowed to trust.
- **Planner · Executor · Critic triad** — one user-initiated Grok run. Score below 85 forces rewrite. Unverified cites are rejected.
- **Matter files** — local intake, captions, counties, parties. Nothing is a court filing.
- **Playbook** — persona, skills, MCP gateway, and the six-step workflow.
- **Stack** — Cole Medin’s 2026 AI-first stack mapped onto this counsel terminal.

Default jurisdiction: New York. Hierarchy is Court of Appeals → the relevant Appellate Division → other departments (persuasive) → trial courts.

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

Without a model key the desk still fills verified templates offline.

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

Output is a drafting aid. Binding effect depends on capacity, consideration, statutory formalities, and a licensed attorney’s review under New York law. The terminal will not pretend a PDF is filed.
