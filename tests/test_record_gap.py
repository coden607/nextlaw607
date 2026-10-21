from nextlaw607.features.record_gap import detect

def test_record_gap_is_case_insensitive_and_deduped():
    assert detect(["Indictment","Transcript","transcript"], ["INDICTMENT"]) == ("Transcript",)
