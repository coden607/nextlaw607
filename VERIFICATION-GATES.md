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

## Legal filing gate

For any generated filing or motion packet, also verify:

1. No unresolved placeholders remain in any document marked filing-ready.
2. Every material factual assertion has a provenance label in the internal work matrix and a corresponding source or explicit unresolved status.
3. Chronology-sensitive claims are checked against available discovery, BWC, transcripts, exhibits, and police/court records.
4. Every material legal proposition is supported by verified authority and a pinpoint citation where available.
5. The strongest adverse authority and prosecution theory were tested.
6. Hearing requests identify the disputed fact, legal issue, burden, and requested relief.
7. Caption, court, judge/local practice, filing method, pagination, exhibits, service, and proposed-order mechanics are verified.
8. Internal notes, uncertainty warnings, and research checklists are not accidentally included in the filed packet.
9. The output status is not `FILING READY` unless all preceding legal filing gates pass.
