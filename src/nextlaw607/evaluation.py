from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


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


class RagasAdapter:
    """Thin adapter around Ragas metrics; scores quality but never legal authority."""

    def __init__(self, *, faithfulness_metric: Any, context_precision_metric: Any) -> None:
        self.faithfulness_metric = faithfulness_metric
        self.context_precision_metric = context_precision_metric

    async def evaluate(
        self,
        *,
        user_input: str,
        response: str,
        retrieved_contexts: Sequence[str],
        reference: str | None = None,
    ) -> RagasScores:
        if not user_input.strip() or not response.strip() or not retrieved_contexts:
            raise ValueError("evaluation inputs must be non-empty")

        common = {
            "user_input": user_input,
            "response": response,
            "retrieved_contexts": list(retrieved_contexts),
        }
        faithfulness_result = await self.faithfulness_metric.ascore(**common)

        precision_input = dict(common)
        if reference is not None:
            precision_input["reference"] = reference
        context_precision_result = await self.context_precision_metric.ascore(**precision_input)

        return RagasScores(
            faithfulness=float(faithfulness_result.value),
            context_precision=float(context_precision_result.value),
        )


class ClaudeEvaluator:
    """Independent supplementary judge. It cannot confer legal-source authority."""

    def __init__(self, *, client: Any, model: str) -> None:
        if not model.strip():
            raise ValueError("model is required")
        self.client = client
        self.model = model

    def evaluate(
        self,
        *,
        question: str,
        answer: str,
        verified_context: Iterable[str],
    ) -> ClaudeJudgeResult:
        context = tuple(item for item in verified_context if item and item.strip())
        if not question.strip() or not answer.strip() or not context:
            return ClaudeJudgeResult(False, 0.0, ("missing verified evaluation input",))

        payload = {
            "question": question,
            "answer": answer,
            "verified_context": context,
        }
        system = (
            "You are an independent legal-answer quality evaluator. Judge only grounding, "
            "scope discipline, and consistency with the supplied already-verified context. "
            "You cannot declare any source good law, verified, authoritative, or citation-safe. "
            "Return strict JSON only with keys passed (boolean), score (0..1), and reasons (array of strings)."
        )
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                system=system,
                messages=[{"role": "user", "content": json.dumps(payload, sort_keys=True)}],
            )
            text = "".join(
                block.text
                for block in getattr(response, "content", ())
                if getattr(block, "type", None) == "text" and isinstance(getattr(block, "text", None), str)
            )
            parsed = json.loads(text)
            if not isinstance(parsed, dict):
                raise ValueError("judge output must be an object")
            passed = parsed.get("passed")
            score = parsed.get("score")
            reasons = parsed.get("reasons", [])
            if not isinstance(passed, bool):
                raise ValueError("passed must be boolean")
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                raise ValueError("score must be numeric")
            if not isinstance(reasons, list) or not all(isinstance(item, str) for item in reasons):
                raise ValueError("reasons must be strings")
            return ClaudeJudgeResult(passed, float(score), tuple(reasons))
        except Exception:
            return ClaudeJudgeResult(False, 0.0, ("malformed or unavailable independent judge output",))


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
