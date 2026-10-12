# NextLaw607 Cloudflare deployment checkpoint

## Goal

Establish a production-shaped Cloudflare Workers Static Assets boundary without weakening deterministic legal trust or exposing server secrets.

## Completed in this milestone

- RED contract for static delivery, HTTPS-only API proxying, fail-closed origin handling, security headers, and secret non-forwarding.
- Worker implementation in `apps/web/worker.mjs` that routes only `/api/*` and `/status/*` to `NEXTLAW_API_ORIGIN` and otherwise serves the `ASSETS` binding.
- Static deployment staging in `apps/web/scripts/build-static.mjs` and the web build script.
- `wrangler.jsonc` using Workers Static Assets with SPA fallback and worker-first API/status routes.
- Exact-revision CI dry-run lane using pinned Wrangler 4.68.0.
- Production-stack manifest records Cloudflare as `implemented`, not `verified`.

## Legal/security invariants

- CitationFirewall remains the authority boundary; the edge worker does not classify, verify, rank, or promote legal authority.
- `NEXTLAW_API_ORIGIN` must be HTTPS; missing/invalid/non-HTTPS configuration fails closed with 503 for API/status routes.
- Cloudflare deployment credentials are never forwarded to the legal API by worker code.
- Static requests do not contact the legal API.
- Server/provider secrets are not embedded in the static bundle.

## Verification evidence

- RED revision: `f4870feea2ec6128bc35bd206c8d0f0c45ecb29a` — `verify` failed after activation of the Cloudflare contract because the worker implementation was absent.
- GREEN behavior revision: `dad1c46afba513dd6467e997b9442f4ebb8ff047` — core `verify` passed with the worker contract enabled.
- Deployment-compat workflow: `.github/workflows/ci.yml#cloudflare-deploy-compat` performs a real Wrangler deploy dry run and asserts an output bundle exists.

## Remaining promotion gate

Do not promote Cloudflare to `verified` until a controlled Cloudflare account/environment performs an actual deployment with `NEXTLAW_API_ORIGIN` supplied through protected configuration, followed by live HTTPS checks of static/PWA routes, API/status proxying, security headers, secret absence, rollback evidence, and exact deployed revision identity.

## Next milestone

After Cloudflare deploy compatibility is green, prioritize Docker runtime verification or the premium frontend accessibility/performance/PWA pass depending on which closes the largest release blocker without requiring provider credentials.
