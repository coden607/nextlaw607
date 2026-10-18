from __future__ import annotations

def build(*, violation_type:str, restitution_balance_known:bool, ability_to_pay_record:bool) -> tuple[str,...]:
    kind=violation_type.strip().lower()
    if kind not in {"technical","new_offense","restitution","mixed"}:
        raise ValueError("unsupported violation type")
    steps=["violation_type","notice_and_procedure","verified_authority","available_remedies"]
    if kind in {"restitution","mixed"}:
        if not restitution_balance_known: steps.append("restitution_balance_gap")
        if not ability_to_pay_record: steps.append("ability_to_pay_record_gap")
    steps.extend(["mitigation","preservation"])
    return tuple(steps)
