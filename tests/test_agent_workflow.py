from dataclasses import replace

from nextlaw607.agents import (
    AgentPhase,
    AgentState,
    AgentWorkflow,
    ToolPolicy,
)
from nextlaw607.authority import LegalAuthority
from nextlaw607.research import LegalResearchRequest


def test_agent_state_is_typed_and_starts_unverified():
    state = AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(),
    )

    assert state.phase is AgentPhase.COLLECT
    assert state.verified_authorities == ()
    assert state.answer is None
    assert state.failure is None


def test_tool_policy_denies_unlisted_tools():
    policy = ToolPolicy(allowed_tools=frozenset({"retrieve_sources"}))

    assert policy.allows("retrieve_sources") is True
    assert policy.allows("shell") is False
    assert policy.allows("browser_write") is False


def test_workflow_requires_deterministic_legal_verification_before_answer():
    unverified = LegalAuthority(
        citation="Fake v Case",
        title="Fake v Case",
        court="Unknown",
        jurisdiction="NY",
        decision_date=__import__("datetime").date(2026, 1, 1),
        source_url="https://example.com/fake",
        source_tier=__import__("nextlaw607.authority", fromlist=["SourceTier"]).SourceTier.SECONDARY,
        holding="Unverified model-supplied text",
    )
    state = AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(unverified,),
    )
    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset()))

    result = workflow.run(state, draft_answer=lambda _: "Treat the candidate as controlling law")

    assert result.phase is AgentPhase.FAILED
    assert result.answer is None
    assert result.verified_authorities == ()
    assert "verified" in (result.failure or "").lower()


def test_model_or_tool_failure_cannot_skip_verification():
    state = AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(),
    )
    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset({"retrieve_sources"})))

    def failing_draft(_state):
        raise RuntimeError("model unavailable")

    result = workflow.run(state, draft_answer=failing_draft)

    assert result.phase is AgentPhase.FAILED
    assert result.answer is None
    assert result.failure is not None


def test_verified_authority_is_the_only_path_to_answer(verified_good_law_authority):
    state = AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(verified_good_law_authority,),
    )
    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset()))

    result = workflow.run(state, draft_answer=lambda s: f"Use {s.verified_authorities[0].authority.citation}")

    assert result.phase is AgentPhase.COMPLETE
    assert result.answer
    assert len(result.verified_authorities) == 1
