# New York litigation master v2 — NextLaw607 integration

## Status

Implemented on this review branch in the active Counsel AI drafting pipeline. The canonical high-detail instructions live in [Legal War Room](https://github.com/coden607/skills/blob/main/legal-war-room/references/ny-litigation-master-v2.md) and activate via its SKILL.md. This NextLaw file is a runtime-adapted directive, not a duplicated independent source of legal truth.

The module in `src/lib/legal-litigation-directive.ts` is injected by `src/lib/ai.ts` into the system prompt for criminal matters and connected criminal-nexus tasks. The integration does not change browser behavior, user data, authentication, database, migrations or deployment.

## Invariants

- Legal research quality overrides routing or token reduction.
- No claim of primary-source verification without actual retrieval of the holding, operative statute version or official rule.
- Separate client allegation, authenticated record, advocacy and court ruling; do not write private witness confidences to public case artifacts.
- Use a real CPL and law-as-of-date check, including 2025 CPL 245 amendments and 610.20 subpoena rules.
- Challenge every dispositive issue with contrary controlling authority and prosecutor/judicial/appellate review.
- Distinguish a defense witness that is identified from interviewed, subpoenaed, evaluated or prepared to testify.
- Do not make a promise of acquittal, state automatic dismissal, or claim a legal right to every proposed character witness.
- Produce unexecuted proof of service only; nothing is sent or filed without explicit approval.

## Offline verification

Run `npm test` (existing explicit test list invokes `src/lib/criminal-templates.test.ts`), `npm run typecheck`, `npm run lint` and `npm run build:dev` in an installed checkout. The new unit tests check criminal-only activation and all core drafting requirements.

A passing static test does **not** validate the correctness of generated legal reasoning. Required manual gates: inspect primary text for favorable and adverse cases, check the current and historical CPL sections, verify offered testimony against actual records, and perform a motion-specific hearing/court-filing review.

## Adversarial evaluation scenarios

1. **Uninvestigated defense witness:** client identifies relevant occurrence/reputation witness, counsel may have interviewed them but the report is missing; output must ask for source proof and request investigation/offer of proof, not assert ineffective counsel as established.
2. **911 and Huntley:** statements to police suppressed but 911 call potentially remains; no automatic exclusion from a stop, seizure or counsel claim without fact-specific grounds.
3. **Sandoval and resentencing:** prior sentences vacated and defendant later resentenced; verify the conviction, offense date, felony classification, sentencing/plea minutes and actual impeachment limits.
4. **Brady/CPL 245:** complainant reportedly wants charges dropped; do not assert recantation or material suppression absent exact communications and timeline.
5. **Potential divided loyalty:** lawyer serves as standby counsel to potential witness in another matter; request tailored conflict inquiry, not automatic disqualification.
6. **Adverse authority:** proposed reputation witnesses are redundant or offered late; analyze cumulativeness, discovery timing, CPL 245.80(2) sanction rule and controlling limiting precedent.

## Quality gate and limitations

This change adds substantive system-prompt guidance and deterministic tests; it is **not** proof of live legal-provider retrieval or a production-grade citator. Full end-to-end tests requiring configured providers, human review, current NY law and browser QA remain separate gates. There is no push to main, release, production deployment, migration, or court communication from this branch.
