from __future__ import annotations

def rank(authorities:list[dict[str,object]], department:str) -> list[dict[str,object]]:
    def key(a:dict[str,object]):
        court=str(a.get("court",""))
        dept=str(a.get("department",""))
        if court=="ny_court_of_appeals": tier=0
        elif court=="ny_appellate_division" and dept==department: tier=1
        elif court=="ny_appellate_division": tier=2
        else: tier=3
        return (tier, -int(a.get("year",0)), str(a.get("citation","")))
    return sorted(authorities,key=key)
