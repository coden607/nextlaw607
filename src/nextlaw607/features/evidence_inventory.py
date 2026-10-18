from __future__ import annotations
import hashlib

def digest(content:bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def audit(items:list[dict[str,object]], required_types:list[str]) -> dict[str,object]:
    seen_hashes:set[str]=set(); types:set[str]=set(); duplicates:list[str]=[]
    for item in items:
        item_type=str(item.get("type","")).strip().lower()
        item_hash=str(item.get("sha256","")).strip().lower()
        if item_type: types.add(item_type)
        if item_hash:
            if item_hash in seen_hashes: duplicates.append(item_hash)
            seen_hashes.add(item_hash)
    missing=sorted({x.lower() for x in required_types}-types)
    return {"missing_types":tuple(missing),"duplicate_hashes":tuple(sorted(set(duplicates)))}
