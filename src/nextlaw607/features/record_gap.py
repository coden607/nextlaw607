from __future__ import annotations

def detect(required: list[str], present: list[str]) -> tuple[str, ...]:
    have={item.strip().lower() for item in present if item.strip()}
    missing={item.strip() for item in required if item.strip() and item.strip().lower() not in have}
    return tuple(sorted(missing, key=str.lower))
