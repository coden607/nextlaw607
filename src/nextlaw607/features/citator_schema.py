from __future__ import annotations
from dataclasses import dataclass

_ALLOWED={"followed","approved","distinguished","limited","criticized","reversed","overruled","unknown"}

@dataclass(frozen=True)
class TreatmentEvidence:
    authority_id:str
    treatment:str
    explicit:bool
    confidence:float
    source_id:str
    def __post_init__(self):
        if self.treatment not in _ALLOWED: raise ValueError("unsupported treatment")
        if not 0.0 <= self.confidence <= 1.0: raise ValueError("confidence out of range")
        if not self.source_id: raise ValueError("source provenance required")
