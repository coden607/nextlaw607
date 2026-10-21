from __future__ import annotations

_LABELS = (
    ("suppression", ("suppress", "huntley", "mapp", "dunaway", "statement", "search", "seizure")),
    ("discovery", ("245", "discovery", "certificate of compliance", "coc")),
    ("speedy_trial", ("30.30", "speedy", "readiness")),
    ("bail", ("bail", "remand", "release")),
    ("grand_jury", ("grand jury", "indictment")),
    ("plea_sentencing", ("plea", "sentence", "sentencing")),
    ("trial_evidence", ("trial", "hearsay", "evidence", "objection")),
    ("appeal", ("appeal", "appellate", "preservation")),
    ("postconviction", ("440", "habeas", "post-conviction", "postconviction")),
    ("probation", ("probation", "restitution", "violation")),
)

def classify(text: str) -> tuple[str, ...]:
    normalized = " ".join(text.lower().split())
    if not normalized:
        return ("unknown",)
    hits = tuple(label for label, terms in _LABELS if any(term in normalized for term in terms))
    return hits or ("general_criminal",)
