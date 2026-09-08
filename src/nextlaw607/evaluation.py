from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeterministicEvalResult:
    passed: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RagasScores:
    faithfulness: float
    context_precision: float

    def __post_init__(self) -> None:
        for name, value in (
            ("faithfulness", self.faithfulness),
            ("context_precision", self.context_precision),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class ClaudeJudgeResult:
    passed: bool
    score: float
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1")


@dataclass(frozen=True)
class EvaluationDecision:
    passed: bool
    label: str
    reasons: tuple[str, ...] = field(default_factory=tuple)


def combine_evaluation(
    *,
    deterministic: DeterministicEvalResult,
    ragas: RagasScores,
    claude: ClaudeJudgeResult,
    min_faithfulness: float = 0.85,
    min_context_precision: float = 0.80,
) -> EvaluationDecision:
    """Combine release-quality signals with deterministic checks as the hard authority gate."""
    if not deterministic.passed:
        return EvaluationDecision(
            passed=False,
            label="DETERMINISTIC_GATE_FAILED",
            reasons=deterministic.reasons,
        )

    if not claude.passed:
        return EvaluationDecision(
            passed=False,
            label="INDEPENDENT_JUDGE_FAILED",
            reasons=claude.reasons,
        )

    quality_reasons: list[str] = []
    if ragas.faithfulness < min_faithfulness:
        quality_reasons.append(
            f"faithfulness {ragas.faithfulness:.3f} below {min_faithfulness:.3f}"
        )
    if ragas.context_precision < min_context_precision:
        quality_reasons.append(
            f"context_precision {ragas.context_precision:.3f} below {min_context_precision:.3f}"
        )
    if quality_reasons:
        return EvaluationDecision(
            passed=False,
            label="RAG_QUALITY_GATE_FAILED",
            reasons=tuple(quality_reasons),
        )

    return EvaluationDecision(passed=True, label="EVALUATION_PASSED")
