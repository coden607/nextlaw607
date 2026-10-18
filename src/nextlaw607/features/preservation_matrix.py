from __future__ import annotations

def assess(*, objection:bool, ruling:bool, constitutional:bool=False) -> dict[str,object]:
    preserved=objection and ruling
    return {
        "preserved":preserved,
        "review_lane":"preserved" if preserved else "interest_of_justice_or_exception",
        "harmless_error_standard":"constitutional" if constitutional else "nonconstitutional",
        "needs_record_prejudice_analysis":True,
    }
