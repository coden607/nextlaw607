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

## Remaining production blockers

This security milestone does not promote any provider-backed component. Release readiness remains fail-closed until genuine evidence exists for Mem0, Langfuse, Sentry, Ragas, Claude evaluator, and Cloudflare deployment/readback/rollback. Final promotion must rerun the complete exact-revision CI, security, privacy, legal, browser, deployment, and `--require-ready` gates.
