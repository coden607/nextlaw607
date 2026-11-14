from __future__ import annotations

from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class LawVersion:
    identifier: str
    effective: date
    expires: date | None = None

def applies(version: LawVersion, on_date: date) -> bool:
    if on_date < version.effective:
        return False
    if version.expires is not None and on_date >= version.expires:
        return False
    return True

def select_applicable(versions: list[LawVersion], on_date: date) -> LawVersion:
    matches = [v for v in versions if applies(v, on_date)]
    if len(matches) != 1:
        raise ValueError("exactly one applicable law version is required")
    return matches[0]
