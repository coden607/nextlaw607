from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class RuleVersion:
    id:str
    effective:date
    end:date|None
    source:str

def select(versions:list[RuleVersion], on_date:date) -> RuleVersion:
    matches=[v for v in versions if v.effective<=on_date and (v.end is None or on_date<v.end)]
    if len(matches)!=1: raise ValueError("rule version is missing or ambiguous")
    return matches[0]
