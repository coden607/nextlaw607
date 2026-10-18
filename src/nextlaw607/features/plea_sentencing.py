from __future__ import annotations

def build(*, plea_offer:bool, conviction_offense_known:bool, predicate_status_known:bool) -> tuple[str,...]:
    if not conviction_offense_known:
        raise ValueError("conviction offense must be known")
    steps=["offense_class","sentencing_exposure","mandatory_discretionary_components","verified_authority"]
    if plea_offer: steps.extend(["plea_terms","waivers","collateral_consequences"])
    if not predicate_status_known: steps.append("predicate_status_gap")
    steps.extend(["mitigation","preservation"])
    return tuple(steps)
