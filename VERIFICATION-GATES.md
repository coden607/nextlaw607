# Verification Gates

Completion requires evidence, not a clean-looking diff.

1. Inspect `git status` and preserve unrelated changes.
2. Run lint, typecheck, tests, and production build.
3. Run browser smoke on the development server at desktop and mobile sizes.
4. Exercise changed interactive flows and inspect console output.
5. Review the diff for secrets, unsafe input handling, and unsupported legal
   claims.
6. Report failed or unavailable gates explicitly; do not call the work fixed,
   secure, deployed, or production-ready without evidence.

Missing external credentials may disable live research or model calls, but
must not disable deterministic offline tests.