from __future__ import annotations

def map_issues(issues:list[dict[str,object]]) -> tuple[dict[str,object],...]:
    out=[]
    for issue in issues:
        name=str(issue.get("issue","")).strip()
        if not name: raise ValueError("issue name required")
        objection=bool(issue.get("objection"))
        ruling=bool(issue.get("ruling"))
        out.append({"issue":name,"preserved":objection and ruling,"objection_anchor":issue.get("objection_anchor"),"ruling_anchor":issue.get("ruling_anchor"),"standard_of_review":issue.get("standard_of_review") or "unresolved"})
    return tuple(out)
