from nextlaw607.features.department_resolver import rank

def test_same_department_precedes_other_department():
    rows=[{"court":"ny_appellate_division","department":"1st","year":2026,"citation":"A"},
          {"court":"ny_appellate_division","department":"3d","year":2025,"citation":"B"}]
    assert rank(rows,"3d")[0]["citation"]=="B"
