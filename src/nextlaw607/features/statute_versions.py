from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class StatuteVersion:
    id:str
    effective:date
    end:date|None
    predecessor:str|None=None

def select(versions:list[StatuteVersion], on_date:date) -> StatuteVersion:
    matches=[v for v in versions if v.effective<=on_date and (v.end is None or on_date<v.end)]
    if len(matches)!=1: raise ValueError("statute version is missing or ambiguous")
    return matches[0]

def lineage(versions:list[StatuteVersion], start_id:str) -> tuple[str,...]:
    by_id={v.id:v for v in versions}; out=[]; cur=by_id.get(start_id)
    while cur:
        out.append(cur.id); cur=by_id.get(cur.predecessor) if cur.predecessor else None
    return tuple(out)
