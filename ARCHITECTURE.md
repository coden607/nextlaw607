# Architecture

NextLaw607 is a Vite-served React and TanStack Router application. The route
tree lives under `src/routes/`, shared UI under `src/components/`, and domain
logic under `src/lib/`.

## Boundaries

- `src/lib/corpus.ts` is the verified internal authority bank.
- `src/lib/courtlistener.ts` and the NY Senate integration are external
  retrieval boundaries; responses require validation before citation.
- `src/lib/ai.ts` is the server-only model boundary. API keys must never reach
  browser code.
- `src/lib/auth/` and `src/lib/app-data/` own authentication and protected data
  access. Authorization must be enforced at the server boundary.
- `src/lib/store.ts` owns local matter state; it is not a filing system.
- `scripts/` contains deterministic build, migration, preview, and validation
  utilities.

## Runtime

`npm run dev` starts Vite on `0.0.0.0:8080` through
`scripts/with-app-env.mjs`. Production build and migration behavior is defined
by `package.json`; do not bypass those scripts with direct Vite commands.

## Change rules

Keep legal retrieval, drafting, critique, authentication, and presentation
separate. Prefer a focused module or test over a cross-cutting refactor. Any
change that affects authority claims must include source-verification coverage.