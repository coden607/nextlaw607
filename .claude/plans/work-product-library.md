# Plan — Work product library + citation provenance + a11y polish

## Audit summary (baseline, all verified on this checkout)

| Check | Command | Exit |
|---|---|---|
| lint | `npm run lint` | 0 (1 pre-existing warning: unused `TEMPLATES` import in `src/lib/criminal-templates.test.ts`) |
| typecheck | `npm run typecheck` | 0 |
| tests | `npm test` | 0 (58 tests, 15 suites) |
| build | `npm run build` | 0 |
| browser smoke | `node scripts/browser-smoke.mjs` (dev, :8080) | 0 — content visible desktop+mobile; 1 console error `ERR_BLOCKED_BY_RESPONSE.NotSameOrigin` = platform `grok.com/extensions.js` CORP block, not app code |
| brand gate | `node scripts/brand-check.mjs --root <repo>` | 0 |
| audit | `npm audit` (via install) | 0 vulnerabilities |

Note: prior-audit claim of a `/jam` police-encounter mode and 66 tests is stale —
verified absent. Current suite is 58 tests, routes are deck/draft/research/triad/matters/intake/playbook/stack.

## Gaps found (traced to PRD/README, no feature theater)

1. **No work-product library.** `DraftRecord`s accumulate in the store (cap 40)
   but the UI only ever surfaces `drafts[0]` (deck) and the latest title per
   matter (matters). A drafting terminal whose output cannot be browsed,
   reviewed, or deleted is incomplete. PRD: "accessible, responsive workflows
   for matters, research, drafting, and critique."
2. **Citation provenance never recorded.** `DraftRecord.citations` is typed but
   always `[]`. The offline fallback path drafts exclusively from the verified
   bank, so its provenance is knowable and must be recorded (PRD req #1:
   "Preserve source provenance for every authority result"). Live model path
   cannot fabricate structured citations — stays `[]` (justified).
3. **A11y polish.** Nav links (desktop + mobile) lack `aria-current`; the
   `ContractPaper` Copy button gives no user feedback (supported `onCopy` prop
   is never passed).
4. **Lint hygiene.** Unused `TEMPLATES` import warning.

## Changes (named files)

1. `src/lib/store.ts` — add `deleteDraft(id: string)` action (also drops from store only; draft list cap already 40).
2. `src/lib/corpus.ts` — add `corpusCitationsForTemplate(tmpl: ContractTemplate): Citation[]`
   mapping `requiredStatutes`/`requiredCases` to verified `Citation` objects
   (`verified: true`, `source: "corpus"`, official URLs from the bank).
3. `src/lib/corpus-citations.test.ts` — NEW. Deterministic test: every template's
   citation list resolves against the bank, all `verified`, `source === "corpus"`,
   statute URLs on nysenate.gov, case URLs non-empty.
4. `package.json` — add `src/lib/corpus-citations.test.ts` to the `npm test` file list.
5. `src/routes/drafts.tsx` — NEW route `/drafts` "Work product": list of all drafts
   (matter caption, template name, score badge, date); selection shows planner
   memo, critic memo, flaws, missing authorities, and the full instrument via
   existing `ContractPaper`; delete button with store action. Mobile-first layout,
   existing Badge/Button components only.
6. `src/components/shell.tsx` — add `Drafts` to `NAV` (icon `FileText`, after Draft);
   add `aria-current="page"` to active desktop + mobile links.
7. `src/routes/draft.tsx` — populate `citations` from `corpusCitationsForTemplate(tmpl)`
   when the payload ran offline; pass `onCopy` toast to `ContractPaper`.
8. `src/lib/criminal-templates.test.ts` — drop unused `TEMPLATES` import (lint warning).
9. `src/routeTree.gen.ts` — regenerate via build (repo convention commits it).

## Out of scope (justified)

- Live-model structured citations: would change the model output contract;
  critic already rejects unverified cites per the zero-hallucination rule.
- PWA/deployment changes: DEPLOYMENT.md gates unchanged; platform chrome untouched.

## Done condition

- `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` all exit 0.
- `node scripts/browser-smoke.mjs` on dev: content visible, no new console errors.
- Playwright: `/drafts` renders drafts, detail view opens, delete removes a draft.
- Diff reviewed: no secrets, no platform-chrome edits, no legal-authority invention.
