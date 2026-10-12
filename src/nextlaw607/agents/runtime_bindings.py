from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import Any

from nextlaw607.agents import AgentState, AgentWorkflow, DraftAnswer


class FrameworkUnavailableError(RuntimeError):
    """Raised when an optional agent framework is not installed or usable."""


Importer = Callable[[str], Any]


def _verified_authority_prompt(state: AgentState) -> str:
    if not state.verified_authorities:
        raise ValueError("drafting requires verified legal authorities")

    authorities = []
    for item in state.verified_authorities:
        authority = item.authority
        authorities.append(
            "\n".join(
                (
                    f"Citation: {authority.citation}",
                    f"Title: {authority.title}",
                    f"Court: {authority.court}",
                    f"Jurisdiction: {authority.jurisdiction}",
                    f"Holding: {authority.holding}",
                    f"Source: {authority.source_url}",
                )
            )
        )

    return (
        "You are drafting a legal research response. Use verified authorities only. "
        "Do not treat model memory, retrieved summaries, or unverified material as legal evidence. "
        "If the verified authorities do not support a proposition, say so rather than inventing support.\n\n"
        f"Question: {state.request.question}\n"
        f"Jurisdiction: {state.request.jurisdiction}\n\n"
        "Verified authorities:\n"
        + "\n\n".join(authorities)
    )


class PydanticAIDraftAdapter:
    """Pydantic AI drafting adapter behind NextLaw's deterministic trust boundary."""

    def __init__(self, *, agent: Any) -> None:
        if agent is None or not callable(getattr(agent, "run_sync", None)):
            raise ValueError("Pydantic AI agent must provide run_sync")
        self._agent = agent

    @classmethod
    def from_model(
        cls,
        model: str,
        *,
        importer: Importer = import_module,
        **agent_kwargs: Any,
    ) -> "PydanticAIDraftAdapter":
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model is required")
        try:
            module = importer("pydantic_ai")
            agent_type = getattr(module, "Agent")
        except (ImportError, AttributeError) as exc:
            raise FrameworkUnavailableError(
                "Pydantic AI is unavailable; install the agent runtime extra before enabling it"
            ) from exc
        try:
            agent = agent_type(model.strip(), **agent_kwargs)
        except Exception as exc:
            raise FrameworkUnavailableError("Pydantic AI agent initialization failed") from exc
        return cls(agent=agent)

    def __call__(self, state: AgentState) -> str:
        prompt = _verified_authority_prompt(state)
        result = self._agent.run_sync(prompt)
        output = getattr(result, "output", None)
        if output is None:
            # Compatibility with older Pydantic AI result objects while the
            # production runtime is version-pinned and independently verified.
            output = getattr(result, "data", None)
        if not isinstance(output, str) or not output.strip():
            raise RuntimeError("Pydantic AI returned no usable text output")
        return output.strip()


class _BoundGraph:
    """Normalizes framework graph invocation to AgentState -> AgentState."""

    def __init__(self, compiled_graph: Any, workflow: AgentWorkflow, draft_answer: DraftAnswer) -> None:
        self._compiled_graph = compiled_graph
        self._workflow = workflow
        self._draft_answer = draft_answer

    def invoke(self, state: AgentState) -> AgentState:
        if not isinstance(state, AgentState):
            raise TypeError("LangGraph binding requires AgentState input")

        def run_workflow() -> AgentState:
            return self._workflow.run(state, draft_answer=self._draft_answer)

        try:
            result = self._compiled_graph.invoke(
                {
                    "state": state,
                    "run_workflow": run_workflow,
                }
            )
        except Exception as exc:
            raise RuntimeError("LangGraph invocation failed closed") from exc

        if isinstance(result, AgentState):
            return result
        if isinstance(result, dict):
            candidate = result.get("result") or result.get("state")
            if isinstance(candidate, AgentState):
                return candidate
        raise RuntimeError("LangGraph returned an invalid state")


class LangGraphBinding:
    """LangGraph adapter that cannot bypass the deterministic AgentWorkflow."""

    def __init__(self, *, graph_factory: Callable[[Any], Any]) -> None:
        self._graph_factory = graph_factory

    @classmethod
    def from_installed(cls, *, importer: Importer = import_module) -> "LangGraphBinding":
        try:
            graph_module = importer("langgraph.graph")
            state_graph = getattr(graph_module, "StateGraph")
        except (ImportError, AttributeError) as exc:
            raise FrameworkUnavailableError(
                "LangGraph is unavailable; install the agent runtime extra before enabling it"
            ) from exc

        def factory(_: Any) -> Any:
            # A dict schema keeps framework state transport separate from the
            # typed AgentState, which remains owned by NextLaw's core.
            return state_graph(dict)

        return cls(graph_factory=factory)

    def compile(self, *, workflow: AgentWorkflow, draft_answer: DraftAnswer) -> _BoundGraph:
        if not isinstance(workflow, AgentWorkflow):
            raise TypeError("workflow must be AgentWorkflow")
        if not callable(draft_answer):
            raise TypeError("draft_answer must be callable")

        try:
            graph = self._graph_factory(dict)

            def legal_workflow(payload: dict[str, Any]) -> dict[str, AgentState]:
                state = payload.get("state")
                runner = payload.get("run_workflow")
                if not isinstance(state, AgentState) or not callable(runner):
                    raise RuntimeError("invalid graph payload")
                result = runner()
                if not isinstance(result, AgentState):
                    raise RuntimeError("deterministic workflow returned invalid state")
                return {"result": result}

            graph.add_node("legal_workflow", legal_workflow)
            graph.set_entry_point("legal_workflow")
            graph.set_finish_point("legal_workflow")
            compiled = graph.compile()
        except Exception as exc:
            raise FrameworkUnavailableError("LangGraph compilation failed") from exc

        return _BoundGraph(compiled, workflow, draft_answer)
