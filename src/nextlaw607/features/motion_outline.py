from __future__ import annotations

def generate(*, issue:str, facts:list[str], authorities:list[dict[str,object]]) -> dict[str,object]:
    if not issue.strip():
        raise ValueError("issue required")
    verified=[a for a in authorities if a.get("verified") is True and a.get("citation") and a.get("source")]
    if not verified:
        raise ValueError("at least one CitationFirewall-approved authority is required")
    return {
        "issue":issue.strip(),
        "sections":("notice_or_relief","facts","governing_law","argument","adverse_authority","conclusion"),
        "facts":tuple(f.strip() for f in facts if f.strip()),
        "authorities":tuple(str(a["citation"]) for a in verified),
    }
