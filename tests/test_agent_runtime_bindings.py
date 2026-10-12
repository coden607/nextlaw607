from datetime import date

from nextlaw607.agents import AgentPhase, AgentState, AgentWorkflow, ToolPolicy
from nextlaw607.agents.runtime_bindings import (
    FrameworkUnavailableError,
    LangGraphBinding,
    PydanticAIDraftAdapter,
)
from nextlaw607.authority import AuthorityStatus, LegalAuthority, SourceTier
from nextlaw607.research import LegalResearchRequest


def verified_authority() -> LegalAuthority:
    return LegalAuthority(
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


def state() -> AgentState:
    return AgentState(
        request=LegalResearchRequest(question="What law controls?", jurisdiction="NY"),
        candidate_authorities=(verified_authority(),),
    )


def test_pydantic_ai_adapter_uses_only_verified_authority_context():
    captured = {}

    class FakeResult:
        output = "Draft grounded in verified authority"

    class FakeAgent:
        def run_sync(self, prompt):
            captured["prompt"] = prompt
            return FakeResult()

    adapter = PydanticAIDraftAdapter(agent=FakeAgent())
    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset()))

    result = workflow.run(state(), draft_answer=adapter)

    assert result.phase is AgentPhase.COMPLETE
    assert result.answer == "Draft grounded in verified authority"
    prompt = captured["prompt"]
    assert "1 N.Y.3d 1" in prompt
    assert "A verified holding." in prompt
    assert "verified authorities only" in prompt.lower()


def test_pydantic_ai_adapter_fails_closed_when_framework_missing():
    try:
        PydanticAIDraftAdapter.from_model("openai:gpt-5", importer=lambda _: (_ for _ in ()).throw(ImportError()))
    except FrameworkUnavailableError as exc:
        assert "pydantic" in str(exc).lower()
    else:
        raise AssertionError("missing Pydantic AI must fail closed")


def test_langgraph_binding_keeps_deterministic_workflow_as_authority_gate():
    events = []

    class FakeCompiledGraph:
        def invoke(self, payload):
            events.append(payload)
            return payload["run_workflow"]()

    class FakeGraph:
        def add_node(self, name, fn):
            assert name == "legal_workflow"
            self.fn = fn

        def set_entry_point(self, name):
            assert name == "legal_workflow"

        def set_finish_point(self, name):
            assert name == "legal_workflow"

        def compile(self):
            return FakeCompiledGraph()

    workflow = AgentWorkflow(tool_policy=ToolPolicy(allowed_tools=frozenset()))
    binding = LangGraphBinding(graph_factory=lambda _: FakeGraph())
    graph = binding.compile(
        workflow=workflow,
        draft_answer=lambda s: f"Use {s.verified_authorities[0].authority.citation}",
    )

    result = graph.invoke(state())

    assert result.phase is AgentPhase.COMPLETE
    assert result.answer == "Use 1 N.Y.3d 1"
    assert events


def test_langgraph_binding_fails_closed_when_framework_missing():
    try:
        LangGraphBinding.from_installed(importer=lambda _: (_ for _ in ()).throw(ImportError()))
    except FrameworkUnavailableError as exc:
        assert "langgraph" in str(exc).lower()
    else:
        raise AssertionError("missing LangGraph must fail closed")
