from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class WarRoomPlan:
    issue: str
    stages: tuple[str, ...]
    requires_verified_authority: bool = True

_KEYWORDS = {
    "suppression": ("facts", "burden", "suppression", "adverse-authority", "draft", "critic"),
    "discovery": ("facts", "cpl-245", "prejudice", "remedy", "adverse-authority", "critic"),
    "speedy": ("timeline", "cpl-30.30", "exclusions", "adverse-authority", "draft", "critic"),
    "appeal": ("record", "preservation", "standard-of-review", "harmless-error", "adverse-authority", "critic"),
}

def dispatch(issue: str) -> WarRoomPlan:
    text = issue.strip().lower()
    if not text:
        raise ValueError("issue is required")
    for key, stages in _KEYWORDS.items():
        if key in text:
            return WarRoomPlan(issue=text, stages=stages)
    return WarRoomPlan(issue=text, stages=("facts", "issue-spot", "authority", "adverse-authority", "draft", "critic"))
