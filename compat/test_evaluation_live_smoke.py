import asyncio
import json
import os
from pathlib import Path

from anthropic import Anthropic
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecision, Faithfulness

from nextlaw607.evaluation import (
    ClaudeEvaluator,
    DeterministicEvalResult,
    RagasAdapter,
    combine_evaluation,
)


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise AssertionError(f"{name} must be configured for the controlled provider smoke")
    return value


def test_real_ragas_and_claude_provider_evaluation_cannot_override_deterministic_gate():
    api_key = _required_env("ANTHROPIC_API_KEY")
    revision = _required_env("NEXTLAW_EXACT_REVISION")
    model = os.environ.get("NEXTLAW_EVAL_MODEL", "claude-sonnet-5").strip() or "claude-sonnet-5"

    client = Anthropic(api_key=api_key, timeout=90.0)
    evaluator_llm = llm_factory(model, provider="anthropic", client=client)
    ragas_adapter = RagasAdapter(
        faithfulness_metric=Faithfulness(llm=evaluator_llm),
        context_precision_metric=ContextPrecision(llm=evaluator_llm),
    )

    question = "Under the synthetic Rule Alpha, what must occur before the action?"
    answer = "Notice must occur before the action."
    verified_context = (
        "Synthetic test context only. Rule Alpha requires notice before the action. ",
        "This text is an evaluation canary and is not legal authority.",
    )
    reference = "Rule Alpha requires notice before the action."

    scores = asyncio.run(
        ragas_adapter.evaluate(
            user_input=question,
            response=answer,
            retrieved_contexts=verified_context,
            reference=reference,
        )
    )
    assert 0.0 <= scores.faithfulness <= 1.0
    assert 0.0 <= scores.context_precision <= 1.0

    claude = ClaudeEvaluator(client=client, model=model)
    judge = claude.evaluate(
        question=question,
        answer=answer,
        verified_context=verified_context,
    )
    assert judge.score > 0.0, judge.reasons
    assert not any("malformed or unavailable" in reason.lower() for reason in judge.reasons)
    assert "authority_eligible" not in judge.__dict__

    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(
            passed=False,
            reasons=("synthetic CitationFirewall failure",),
        ),
        ragas=scores,
        claude=judge,
    )
    assert decision.passed is False
    assert decision.label == "DETERMINISTIC_GATE_FAILED"

    evidence = {
        "schema_version": 1,
        "revision": revision,
        "model": model,
        "ragas": {
            "faithfulness": scores.faithfulness,
            "context_precision": scores.context_precision,
        },
        "claude": {"passed": judge.passed, "score": judge.score},
        "deterministic_override_test": decision.label,
        "authority_eligible": False,
        "verified_authority": False,
    }
    rendered = json.dumps(evidence, sort_keys=True)
    assert api_key not in rendered
    assert question not in rendered
    assert answer not in rendered
    assert all(item not in rendered for item in verified_context)
    Path("evaluation-live-evidence.json").write_text(rendered + "\n", encoding="utf-8")
