from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from anthropic import Anthropic, AsyncAnthropic
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecision, Faithfulness

from nextlaw607.evaluation import (
    ClaudeEvaluator,
    DeterministicEvalResult,
    RagasScores,
    combine_evaluation,
)


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required provider configuration: {name}")
    return value


async def _run_ragas(*, api_key: str, model: str) -> RagasScores:
    client = AsyncAnthropic(api_key=api_key, timeout=60.0, max_retries=2)
    llm = llm_factory(model, client=client)

    context = [
        "Synthetic verified test context: Example Rule 1 requires the filing by Friday."
    ]
    question = "When does Example Rule 1 require the filing?"
    answer = "Example Rule 1 requires the filing by Friday."
    reference = "The filing is due Friday."

    faithfulness = Faithfulness(llm=llm)
    precision = ContextPrecision(llm=llm)

    faithfulness_result = await faithfulness.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=context,
    )
    precision_result = await precision.ascore(
        user_input=question,
        reference=reference,
        retrieved_contexts=context,
    )

    return RagasScores(
        faithfulness=float(faithfulness_result.value),
        context_precision=float(precision_result.value),
    )


def test_provider_backed_ragas_and_claude_verification():
    api_key = _required("ANTHROPIC_API_KEY")
    model = _required("ANTHROPIC_EVAL_MODEL")
    revision = _required("NEXTLAW_EXACT_REVISION")

    ragas_scores = asyncio.run(_run_ragas(api_key=api_key, model=model))

    context = (
        "Synthetic verified test context: Example Rule 1 requires the filing by Friday.",
    )
    question = "When does Example Rule 1 require the filing?"
    answer = "Example Rule 1 requires the filing by Friday."

    claude = ClaudeEvaluator(client=Anthropic(api_key=api_key), model=model).evaluate(
        question=question,
        answer=answer,
        verified_context=context,
    )
    decision = combine_evaluation(
        deterministic=DeterministicEvalResult(True),
        ragas=ragas_scores,
        claude=claude,
        min_faithfulness=0.80,
        min_context_precision=0.80,
    )

    assert decision.passed, decision.reasons

    Path("evaluation-live-evidence.json").write_text(
        json.dumps(
            {
                "provider": "anthropic+ragaS",
                "model": model,
                "revision": revision,
                "faithfulness": ragas_scores.faithfulness,
                "context_precision": ragas_scores.context_precision,
                "claude_passed": claude.passed,
                "claude_score": claude.score,
                "decision": decision.label,
                "authority_eligible": False,
            },
            sort_keys=True,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
