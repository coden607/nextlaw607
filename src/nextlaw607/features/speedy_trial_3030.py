from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Period:
    start:date
    end:date
    excludable:bool=False
    reason:str=""

def chargeable_days(periods:list[Period]) -> int:
    total=0
    for p in periods:
        if p.end < p.start: raise ValueError("period end precedes start")
        if not p.excludable:
            total += (p.end-p.start).days
    return total
