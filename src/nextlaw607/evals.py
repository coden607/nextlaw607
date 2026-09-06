from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

@dataclass(frozen=True)
class LegalEvalCase:
    id: str
    input: dict
    must_include: tuple[str, ...]
    must_not_include: tuple[str, ...]

@dataclass(frozen=True)
class LegalEvalResult:
    id: str
    passed: bool
    missing: tuple[str, ...]
    forbidden_found: tuple[str, ...]

@dataclass(frozen=True)
class LegalEvalReport:
    results: tuple[LegalEvalResult, ...]
    @property
    def passed(self) -> bool: return bool(self.results) and all(r.passed for r in self.results)
    @property
    def pass_rate(self) -> float: return sum(r.passed for r in self.results)/len(self.results) if self.results else 0.0

class LegalEvalRunner:
    def load(self, path: str | Path) -> tuple[LegalEvalCase, ...]:
        raw=json.loads(Path(path).read_text())
        return tuple(LegalEvalCase(
            id=item['id'], input=item['input'], must_include=tuple(item.get('must_include',())),
            must_not_include=tuple(item.get('must_not_include',()))
        ) for item in raw)

    def run(self, cases: tuple[LegalEvalCase, ...], executor: Callable[[dict], str]) -> LegalEvalReport:
        results=[]
        for case in cases:
            output=executor(case.input).lower()
            missing=tuple(term for term in case.must_include if term.lower() not in output)
            forbidden=tuple(term for term in case.must_not_include if term.lower() in output)
            results.append(LegalEvalResult(case.id, not missing and not forbidden, missing, forbidden))
        return LegalEvalReport(tuple(results))
