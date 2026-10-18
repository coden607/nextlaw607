from __future__ import annotations

def classify(*, source:str, issue_basis:str, state_protection_broader:bool=False) -> str:
    if source=="us_supreme_court" and issue_basis in {"federal","both"}:
        return "federal_controlling"
    if source=="ny_court_of_appeals" and issue_basis in {"state","both"}:
        return "state_controlling_broader" if state_protection_broader else "state_controlling"
    return "candidate_persuasive"
