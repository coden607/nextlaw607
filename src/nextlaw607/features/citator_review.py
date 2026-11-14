from __future__ import annotations
from .citator_schema import TreatmentEvidence

def needs_review(item:TreatmentEvidence, *, threshold:float=0.85) -> bool:
    return (not item.explicit) or item.confidence < threshold or item.treatment=="unknown"

def build_queue(items:list[TreatmentEvidence], *, threshold:float=0.85) -> tuple[TreatmentEvidence,...]:
    return tuple(sorted((x for x in items if needs_review(x,threshold=threshold)), key=lambda x:(x.confidence,x.authority_id)))
