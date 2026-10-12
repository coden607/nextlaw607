# NextLaw607 PWA Offline Legal-Data Safety Checkpoint

## Goal
Preserve resilient offline PWA navigation without allowing legal API/status payloads to enter Cache Storage or allowing an offline API failure to masquerade as the cached application shell.

## Trust boundary
CitationFirewall remains the only legal-authority promotion boundary. Service-worker cache state, browser state, memory, retrieval output, and model output are never legal evidence. `/api/*` and `/status/*` are network-only at the service-worker layer.

## TDD evidence
- Prior frontend-quality GREEN checkpoint: `beeb8295e33488a71a7bd09001828590d7301261`; CI `34237095500` and Browser release evidence `34237095439` passed.
- RED test definition: `3db2a7b115e3680e60f473706b5da993e9f9fc7c`.
- RED activation: `41a301fb28a52b54814d917198a5411bf5b65056`; Browser release evidence `34243845300` failed at `Verify release gates`, and CI run `34243845230` failed in `verify` while unrelated compatibility jobs remained green.
- Minimal service-worker GREEN implementation: `be1af8e21ef4534b5ee4287a2dd1453eb450fefc`.
- Test-environment correction only: `2f99f7b1103801a5d3b9136efa83fad5315205a9`, adding the standard worker `URL` global to the VM harness without relaxing privacy assertions.
- Exact-sha `verify` passed on CI run `34244216468`; Browser release evidence `34244216492` passed.

## Verified behavior
- Successful `/api/*` and `/status/*` GET responses are not written to Cache Storage.
- Offline `/api/*` and `/status/*` requests fail as backend requests; they never fall back to `/` or another cached app-shell response.
- Non-backend static resources retain network-first cache fallback.
- Navigation requests may fall back to the cached application shell when offline.
- Cache namespace advanced to `nextlaw607-v0.2.2`, allowing prior cache cleanup during activation.

## Remaining production blockers
- Actual controlled Cloudflare deployment using protected `NEXTLAW_API_ORIGIN`, followed by live HTTPS/static/PWA/API/status/security-header/revision/rollback checks.
- Provider-backed Mem0 add/export/delete/re-query verification.
- Configured NeMo rails smoke verification with deterministic NextLaw gates first.
- Controlled external telemetry export verification.
- Provider-backed Ragas/Claude evaluation verification.
- Archon and n8n development/orchestration integrations only; neither may become legal-authority logic.
- Final clean-checkout security/privacy/legal/deployment release verification before PR #7 leaves draft status.
