from __future__ import annotations

_BASE=("discoverable_material_inventory","automatic_disclosure","due_date","certificate_of_compliance","readiness_link","prejudice","sanction_or_remedy","verified_authority")

def build(*, coc_filed:bool, readiness_announced:bool) -> tuple[str,...]:
    steps=list(_BASE)
    if readiness_announced and not coc_filed:
        steps.append("readiness_validity_review")
    if not coc_filed:
        steps.append("coc_gap")
    return tuple(steps)
