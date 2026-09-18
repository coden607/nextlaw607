# Deployment

The application is intended for Vercel deployment using the generated Nitro
output. Deployment must supply server-only environment variables through the
provider secret manager; never commit or bake them into browser bundles.

## Required checks

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
```

`DATABASE_URL` enables the PostgreSQL deployment path. Without it, the local
PGlite fallback is used where supported. Apply migrations through the
repository migration process before enabling production auth/data flows.

## Environment

See `.env.example` for variable names only. `XAI_API_KEY`,
`COURTLISTENER_API_TOKEN`, and `NYSENATE_API_KEY` are server-only. Rotate a key
at the provider if exposure is suspected.

## Release safety

Do not deploy from a dirty worktree without reviewing the diff. Confirm the
production build, auth invariant, source provenance behavior, and browser smoke
results before release. Do not treat a successful deployment as legal or
research validation.