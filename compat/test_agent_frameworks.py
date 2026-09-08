from datetime import date

from pydantic_ai import Agent, models
from pydantic_ai.models.test import TestModel

from nextlaw607.agents import AgentPhase, AgentState, AgentWorkflow, ToolPolicy
from nextlaw607.agents.runtime_bindings import LangGraphBinding, PydanticAIDraftAdapter
from nextlaw607.authority import AuthorityStatus, LegalAuthority, SourceTier
from nextlaw607.research import LegalResearchRequest


models.ALLOW_MODEL_REQUESTS = False


def _state() -> AgentState:
    authority = LegalAuthority(
        citation="1 N.Y.3d 1",
        title="People v Example",
        court="NY Court of Appeals",
        jurisdiction="NY",
        decision_date=date(2024, 1, 1),
        source_url="https://nycourts.gov/example",
        source_tier=SourceTier.OFFICIAL,
        holding="A verified holding.",
        status=AuthorityStatus.GOOD_LAW,
        last_verified_on=date.today(),
        verification_sources=("https://nycourts.gov/example",),
        citation_history_checked_on=date.today(),
        negative_treatment_found=False,
        history_sources=("https://www.courtlistener.com/opinion/123/example/",),
    )
    return AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(authority,),
    )


def test_installed_pydantic_ai_and_langgraph_preserve_nextlaw_trust_boundary():
    agent = Agent(TestModel(custom_output_text="Framework-compatible verified draft"))
    draft_adapter = PydanticAIDraftAdapter(agent=agent)
    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset()))
    graph = LangGraphBinding.from_installed().compile(
        workflow=workflow,
        draft_answer=draft_adapter,
    )

    result = graph.invoke(_state())

    assert result.phase is AgentPhase.COMPLETE
    assert result.answer == "Framework-compatible verified draft"
    assert len(result.verified_authorities) == 1
    assert result.verified_authorities[0].authority.citation == "1 N.Y.3d 1"
