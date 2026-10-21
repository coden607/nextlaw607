from __future__ import annotations

_COURT_WEIGHT = {
    "us_supreme_court": 100,
    "ny_court_of_appeals": 95,
    "second_circuit": 90,
    "ny_appellate_division": 80,
    "ny_appellate_term": 65,
    "ny_trial_court": 50,
    "other": 20,
}

def score_authority(*, court: str, jurisdiction_match: bool, department_match: bool = False, current: bool = True) -> int:
    score = _COURT_WEIGHT.get(court, _COURT_WEIGHT["other"])
    if jurisdiction_match:
        score += 10
    if department_match:
        score += 5
    if not current:
        score -= 40
    return max(score, 0)
