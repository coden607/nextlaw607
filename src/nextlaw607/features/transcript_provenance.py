from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TranscriptSpan:
    page:int
    start_line:int
    end_line:int
    text:str

def make_span(*, page:int,start_line:int,end_line:int,text:str) -> TranscriptSpan:
    if page < 1 or start_line < 1 or end_line < start_line:
        raise ValueError("invalid transcript anchor")
    if not text.strip():
        raise ValueError("transcript text required")
    return TranscriptSpan(page,start_line,end_line,text.strip())

def anchor(span:TranscriptSpan) -> str:
    return f"p.{span.page}:L{span.start_line}-L{span.end_line}"
