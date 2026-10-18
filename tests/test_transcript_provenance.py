import pytest
from nextlaw607.features.transcript_provenance import make_span, anchor

def test_transcript_anchor_is_stable():
    s=make_span(page=12,start_line=3,end_line=7,text=" testimony ")
    assert anchor(s)=="p.12:L3-L7" and s.text=="testimony"

def test_invalid_anchor_fails():
    with pytest.raises(ValueError): make_span(page=0,start_line=1,end_line=1,text="x")
