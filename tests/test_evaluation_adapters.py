import asyncio

from nextlaw607.evaluation import ClaudeEvaluator, ClaudeJudgeResult, RagasAdapter, RagasScores


class _MetricResult:
    def __init__(self, value: float) -> None:
        self.value = value


class _Metric:
    def __init__(self, value: float) -> None:
        self.value = value
        self.calls = []

    async def ascore(self, **kwargs):
        self.calls.append(kwargs)
        return _MetricResult(self.value)


class _Messages:
    def __init__(self, text: str) -> None:
        self.text = text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        block = type("Block", (), {"type": "text", "text": self.text})()
        return type("Response", (), {"content": [block]})()


class _ClaudeClient:
    def __init__(self, text: str) -> None:
        self.messages = _Messages(text)


def test_ragas_adapter_returns_bounded_quality_scores_without_authority_promotion():
    faithfulness = _Metric(0.91)
    context_precision = _Metric(0.87)
    adapter = RagasAdapter(
        faithfulness_metric=faithfulness,
        context_precision_metric=context_precision,
    )

    scores = asyncio.run(
        adapter.evaluate(
            user_input="What is the controlling rule?",
            response="A grounded answer.",
            retrieved_contexts=["Verified authority text."],
            reference="Expected grounded answer.",
        )
    )

    assert scores == RagasScores(faithfulness=0.91, context_precision=0.87)
    assert faithfulness.calls
    assert context_precision.calls


def test_claude_evaluator_requires_strict_json_and_cannot_claim_authority():
    client = _ClaudeClient(
        '{"passed": false, "score": 0.4, "reasons": ["overstates the holding"], "authority_eligible": true}'
    )
    evaluator = ClaudeEvaluator(client=client, model="claude-sonnet-5")

    result = evaluator.evaluate(
        question="What does the case hold?",
        answer="Draft answer",
        verified_context=["Verified authority excerpt"],
    )

    assert result == ClaudeJudgeResult(
        passed=False,
        score=0.4,
        reasons=("overstates the holding",),
    )
    assert "authority_eligible" not in result.__dict__


def test_claude_evaluator_fails_closed_on_malformed_or_non_json_output():
    evaluator = ClaudeEvaluator(client=_ClaudeClient("not-json"), model="claude-sonnet-5")

    result = evaluator.evaluate(
        question="question",
        answer="answer",
        verified_context=["context"],
    )

    assert result.passed is False
    assert result.score == 0.0
    assert "malformed" in result.reasons[0].lower()
