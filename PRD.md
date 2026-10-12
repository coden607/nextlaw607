# Product Requirements

## Product

NextLaw607 is a New York legal-intelligence terminal for attorneys and the
public. It supports matter intake, authority discovery, drafting assistance,
and adversarial review. It is not a law firm, a court filing system, or legal
advice.

## Requirements

- Preserve source provenance for every authority result.
- Prefer controlling New York authority by court, department, jurisdiction,
  issue, and date.
- Keep public self-help material separate from citable primary authority.
- Fail closed on unverified citations and label research gaps.
- Keep external model and provider calls user-initiated, bounded, and server-only.
- Support accessible, responsive workflows for matters, research, drafting, and
  critique.
- Preserve offline verified templates and deterministic tests when providers are
  unavailable.

## Non-goals

- Replacing LexisNexis, Westlaw, Shepard's, or KeyCite.
- Representing that a result is current, controlling, or procedurally complete
  without source verification.
- Filing documents or creating an attorney-client relationship.

## Criminal Defense Module (v2)

Adds a dedicated criminal-defense instrument set and doctrine bank on top of
the existing `criminal` practice area:

- **Three new instruments** (`src/lib/templates.ts`):
  - `criminal-retention` — defense engagement letter with scope limits, fee
    placeholder, investigation budget, and client-duty recitals.
  - `mitigation-memo` — sentencing mitigation skeleton (client history,
    treatment, restitution, and statutory mitigation / CPL Art. 720
    youthful-offender placeholders).
  - `suppression-brief` — motion-to-suppress skeleton (CPL 710) with
    stop/search/seizure fact placeholders, standing section, and
    fruit-of-the-poisonous-tree paragraphs.
- **Corpus expansion** (`src/lib/corpus.ts`): Penal Law Articles 120, 125,
  130, 140, 155, 160, 220, 265; CPL 140.20, 710.20, 710.40, 450.10, 470.05;
  landmark authorities — Mapp, Miranda, Terry, Dunaway, Wong Sun, Brady,
  Batson, Crawford (U.S. Supreme Court) and People v. Huntley (N.Y.).
  Citation-honesty rule: only verifiable authority enters the bank; the
  header comment states that an attorney must verify all citations.
- **Persona evolution** (`src/lib/skills.ts`): the system persona now adopts
  a high-dollar NY criminal-defense counsel voice — burden-of-proof obsessed,
  preservation-of-error instinct, admissibility-first — while still
  disclaiming that it is not legal advice.
- **Tests** (`src/lib/criminal-templates.test.ts`): deterministic render + 
  corpus-integrity checks.

**Attorney-review requirement:** every criminal instrument is a drafting
scaffold. A licensed New York attorney must review, verify every citation,
and approve before any document is filed, served, or signed.