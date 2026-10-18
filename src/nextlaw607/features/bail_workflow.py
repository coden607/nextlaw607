from __future__ import annotations

def build(*, qualifying_offense:bool|None, risk_of_flight_facts:bool, current_order:bool) -> tuple[str,...]:
    if qualifying_offense is None:
        raise ValueError("qualifying-offense status must be verified")
    steps=["procedural_posture","qualifying_offense_check","least_restrictive_conditions","verified_authority"]
    if risk_of_flight_facts: steps.append("flight_risk_record")
    if current_order: steps.append("changed_circumstances_or_review_basis")
    return tuple(steps)
