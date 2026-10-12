from nextlaw607.evaluation import (
    ClaudeJudgeResult,
    DeterministicEvalResult,
    EvaluationDecision,
    RagasScores,
    combine_evaluation,
)


def test_deterministic_failure_cannot_be_overridden_by_llm_or_ragas_scores():
    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(passed=False, reasons=("citation firewall failed",)),
        ragas=RagasScores(faithfulness=1.0, context_precision=1.0),
        claude=ClaudeJudgeResult(passed=True, score=1.0, reasons=("looks excellent",)),
    )

    assert isinstance(decision, EvaluationDecision)
    assert decision.passed is False
    assert decision.label == "DETERMINISTIC_GATE_FAILED"
    assert "citation firewall failed" in decision.reasons


def test_llm_judge_failure_can_block_promotion_after_deterministic_pass():
    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(passed=True),
        ragas=RagasScores(faithfulness=0.95, context_precision=0.90),
        claude=ClaudeJudgeResult(passed=False, score=0.3, reasons=("answer overstates authority",)),
    )

    assert decision.passed is False
    assert decision.label == "INDEPENDENT_JUDGE_FAILED"


def test_ragas_thresholds_are_supplementary_but_can_block_release_quality_gate():
    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(passed=True),
        ragas=RagasScores(faithfulness=0.70, context_precision=0.90),
        claude=ClaudeJudgeResult(passed=True, score=0.95),
        min_faithfulness=0.85,
        min_context_precision=0.80,
    )

    assert decision.passed is False
    assert decision.label == "RAG_QUALITY_GATE_FAILED"


def test_all_evaluation_layers_must_pass_for_release_quality_gate():
    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(passed=True),
        ragas=RagasScores(faithfulness=0.93, context_precision=0.91),
        claude=ClaudeJudgeResult(passed=True, score=0.92),
        min_faithfulness=0.85,
        min_context_precision=0.80,
    )

    assert decision.passed is True
    assert decision.label == "EVALUATION_PASSED"
