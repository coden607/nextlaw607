from __future__ import annotations

_COMMON=("identify_evidence","identify_police_conduct","standing_or_personal_right","burden_map","verified_authority","adverse_authority","remedy")
_EXTRA={
 "statement":("custody","interrogation","warnings","voluntariness"),
 "physical":("search_or_seizure","warrant_or_exception","causation"),
 "identification":("procedure","suggestiveness","independent_source"),
}

def build(evidence_type:str) -> tuple[str,...]:
    kind=evidence_type.strip().lower()
    if kind not in _EXTRA: raise ValueError("unsupported suppression evidence type")
    return _COMMON+_EXTRA[kind]
