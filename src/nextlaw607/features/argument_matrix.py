from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ArgumentRow:
    issue:str
    argument:str
    counterargument:str
    burden:str
    standard_of_review:str
    authority_ids:tuple[str,...]

def build(rows:list[dict[str,object]]) -> tuple[ArgumentRow,...]:
    out=[]
    for row in rows:
        issue=str(row.get("issue","")).strip()
        argument=str(row.get("argument","")).strip()
        counter=str(row.get("counterargument","")).strip()
        burden=str(row.get("burden","")).strip()
        standard=str(row.get("standard_of_review","")).strip()
        ids=tuple(str(x) for x in row.get("authority_ids",()) if str(x).strip())
        if not all((issue,argument,counter,burden,standard)) or not ids:
            raise ValueError("argument rows require both sides, burden, standard, and verified authority ids")
        out.append(ArgumentRow(issue,argument,counter,burden,standard,ids))
    return tuple(out)
