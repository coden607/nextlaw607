from __future__ import annotations

def classify_claims(claims:list[dict[str,object]]) -> tuple[dict[str,str],...]:
    out=[]
    for claim in claims:
        name=str(claim.get("claim","")).strip()
        if not name: raise ValueError("claim required")
        record_support=bool(claim.get("record_support"))
        extra_record=bool(claim.get("extra_record_support"))
        if record_support and not extra_record: lane="record"
        elif extra_record and not record_support: lane="extra_record"
        elif record_support and extra_record: lane="mixed"
        else: lane="unsupported"
        out.append({"claim":name,"lane":lane})
    return tuple(out)
