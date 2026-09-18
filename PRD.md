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