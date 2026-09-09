# NextLaw607 Release Security Verification Checkpoint

## Purpose

Add a credential-independent, exact-revision security gate to the 2026 production-stack release path without changing legal authority semantics or weakening provider/deployment readiness requirements.

## Trust boundary

CitationFirewall remains the only path for promoting legal authority. Security scanners, dependency audits, memory, model output, telemetry, evaluation scores, and orchestration output are never legal evidence.

## TDD evidence

- RED commit `8677a72c9b37d59291bcccab0db64823475e384a` added `tests/test_security_release_gate.py` before implementation.
- RED CI run `34406087469`, job `verify` / `102649279355`, failed only because `.github/workflows/security.yml` did not exist: `1 failed, 261 passed`.
- GREEN commit `8ac8d991df43126b593b200653b34e92efa03e44` added `.github/workflows/security.yml`.
- Security run `34406201764` passed exact-revision checkout assertions, Gitleaks, isolated Python `pip-audit`, and npm high-severity audit.
- The same GREEN revision passed the core `verify` job in CI run `34406201708`; browser, Supabase RLS, OpenTelemetry, Archon, and n8n gates also passed for that revision.

## Gate contract

- read-only repository permissions
- exact PR-head/SHA checkout with persisted Git credentials disabled
- secret scan via Gitleaks
- isolated Python dependency audit via `pip-audit --local`
- web dependency audit via `npm audit --audit-level=high`
- scheduled weekly drift detection in addition to push/PR execution

## Secret bootstrap checkpoint

The provider/deployment configuration path now has a fail-closed, names-only secret manifest and idempotent CLI bootstrap. Secret values are never committed or written into recovery evidence.

- RED commit `74d098c0f06695d5a42fd3b97e2b481434d7be8d` added `tests/test_secret_bootstrap_contract.py` first.
- RED CI run `34407842692`, verify job `102654990977`, failed exactly because `config/secrets.manifest` was absent, with `262 passed, 1 failed`.
- Implementation commits `50b7aef1dca770f9a0d155c7e91f0f7ee3e99401`, `cd5b6f14c632fc87425201eb4bd3f0f9943eb373`, and `b44d820efd0fe7624dc49156e333214479ecac7c` added the names-only manifest, bootstrap script, and corrected GitHub CLI secret streaming.
- GREEN hardening commit `3ad6d85dbf5f82063e5f93f751eccbe508df3070` preserves existing GitHub secret/variable names unless `NEXTLAW_FORCE_SECRET_REFRESH=1` is explicitly set and checks Cloudflare secret names without retrieving secret values.
- Exact-head CI run `34408297269` passed all 12 jobs. The `verify` job `102656462417` passed `263` Python tests plus `25/25` web/PWA tests, validated all JSON manifests, and confirmed the production-stack contract covers all `22` approved components.
- The same exact revision passed Browser release evidence `34408297133`, Security release gate `34408297130`, Supabase RLS `34408297065`, OpenTelemetry `34408297162`, Archon `34408297183`, and n8n `34408297091`.
- Cloudflare deploy compatibility passed as a Wrangler exact-revision dry run only; this is not live deployment evidence.

## Remaining production blockers

This checkpoint does not promote any provider-backed component. Release readiness remains fail-closed until genuine evidence exists for Mem0, Langfuse, Sentry, Ragas, Claude evaluator, and Cloudflare deployment/readback/rollback. The previously stale exact-head verification blocker is closed for revision `3ad6d85dbf5f82063e5f93f751eccbe508df3070`; any later documentation or code commit must itself re-close the exact-head gates before promotion. Final promotion must rerun the complete exact-revision CI, security, privacy, legal, browser, deployment, and `--require-ready` gates.
