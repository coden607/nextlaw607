from __future__ import annotations

def build(evidence: list[dict[str,object]]) -> tuple[dict[str,object],...]:
    out=[]
    for item in evidence:
        name=str(item.get("name","")).strip()
        if not name: raise ValueError("evidence name required")
        out.append({"name":name,"foundation":bool(item.get("foundation")),"objection":item.get("objection") or "unassessed","provenance":item.get("provenance") or "missing"})
    return tuple(out)
