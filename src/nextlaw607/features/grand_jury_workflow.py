from __future__ import annotations

def build(*, indictment_present:bool, grand_jury_minutes_available:bool, preservation_known:bool) -> tuple[str,...]:
    steps=["indictment_elements","jurisdiction","timeliness","verified_authority"]
    if not indictment_present: steps.append("missing_indictment")
    if not grand_jury_minutes_available: steps.append("minutes_access_or_review_gap")
    if not preservation_known: steps.append("preservation_gap")
    steps.extend(["defect_screen","remedy_screen"])
    return tuple(steps)
