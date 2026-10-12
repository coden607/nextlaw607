from __future__ import annotations

import pytest

from nextlaw607.orchestration import DevelopmentOrchestrator, OrchestrationPolicyError


def test_archon_and_n8n_are_development_only_and_cannot_promote_legal_authority() -> None:
    orchestrator = DevelopmentOrchestrator(allowed_tools={"pytest", "ruff", "npm-test"})

    task = orchestrator.prepare_task(
        engine="archon",
        objective="Run the legal-core regression suite",
        requested_tools=["pytest"],
        payload={"candidate_text": "People v. Example", "authority_eligible": True},
    )

    assert task.engine == "archon"
    assert task.scope == "development-only"
    assert task.payload["authority_eligible"] is False
    assert task.payload["trusted"] is False
    assert task.payload["verified_authority"] is False


def test_n8n_task_rejects_unapproved_tools_and_secret_like_payloads() -> None:
    orchestrator = DevelopmentOrchestrator(allowed_tools={"pytest"})

    with pytest.raises(OrchestrationPolicyError, match="tool is not allowlisted"):
        orchestrator.prepare_task(
            engine="n8n",
            objective="Run tests",
            requested_tools=["shell"],
            payload={},
        )

    with pytest.raises(OrchestrationPolicyError, match="secret-like field"):
        orchestrator.prepare_task(
            engine="n8n",
            objective="Run tests",
            requested_tools=["pytest"],
            payload={"api_key": "do-not-forward"},
        )


def test_orchestration_rejects_unknown_engines() -> None:
    orchestrator = DevelopmentOrchestrator(allowed_tools={"pytest"})

    with pytest.raises(OrchestrationPolicyError, match="unsupported orchestration engine"):
        orchestrator.prepare_task(
            engine="untrusted-agent",
            objective="Run tests",
            requested_tools=["pytest"],
            payload={},
        )
