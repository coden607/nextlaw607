from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BenchmarkResult:
    total:int
    correct:int
    accuracy:float
    failed_closed:int

def evaluate(predicted:list[str], gold:list[str]) -> BenchmarkResult:
    if len(predicted)!=len(gold):
        raise ValueError("prediction and gold lengths differ")
    total=len(gold)
    correct=sum(a==b for a,b in zip(predicted,gold))
    failed=sum(a=="unknown" for a in predicted)
    return BenchmarkResult(total,correct,(correct/total if total else 1.0),failed_closed=failed)
