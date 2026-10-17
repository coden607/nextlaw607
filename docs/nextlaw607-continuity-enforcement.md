# NextLaw607 Continuity enforcement contract

## Goal

Every coding agent that can read this repository must discover the same engineering route without depending on conversation memory or vendor-specific prompts.

## Required route

agent -> AGENTS.md -> Continuity preflight -> canonical coden607/skills -> Jev/token/security gates -> applicable legal/product skills -> implementation and verification -> PR -> protected main.

During migration, the current Continuity OS remains the required orchestration entrypoint. Retire it only after Continuity OS Base capabilities are integrated into NextLaw607 and the replacement passes documented parity, security, provenance, and regression gates.

## Defense in depth

1. AGENTS.md is the portable discovery contract.
2. scripts/continuity-preflight.sh deterministically checks the repository contract and, when mounted, the real Continuity CLI and canonical skill library.
3. .github/workflows/continuity-contract.yml runs that preflight on every pull request and push to main.
4. Existing verify, lint, typecheck, tests, build, browser smoke, auth, and security checks remain independent. Continuity enforcement never replaces them.
5. GitHub branch protection/rulesets should require continuity-contract plus existing required CI. Never use admin bypass or force merge as the normal path.
6. CitationFirewall and legal provenance requirements fail closed; they cannot be weakened for cost or convenience.

## Portability

No Claude-, Codex-, Gemini-, Kimi-, Grok-, or Copilot-specific file is the sole control. Vendor adapters may point to AGENTS.md, but repository-readable contracts plus deterministic CI are canonical.

## Transition gate

Old Continuity OS can be retired only when all of these have evidence: stable Continuity Base NextLaw entrypoint; canonical skill loading; Jev/routing; token optimization; interrupts; isolation; second brain; hooks/guardrails; Software Factory parity; legal provenance/CitationFirewall tests; security/regression checks; and an updated architecture decision recording cutover.

Until then, current Continuity remains mandatory for substantive NextLaw engineering.
