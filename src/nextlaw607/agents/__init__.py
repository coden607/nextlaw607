from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum

from nextlaw607.authority import CitationFirewall, LegalAuthority
from nextlaw607.research import LegalResearchRequest, ResearchWorkflow, VerifiedAuthority


class AgentPhase(str, Enum):
    COLLECT = "collect"
    VERIFY = "verify"
    DRAFT = "draft"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(frozen=True)
class ToolPolicy:
    """Deterministic allowlist for tools exposed to an agent runtime."""

    allowed_tools: frozenset[str]

    def allows(self, tool_name: str) -> bool:
        return bool(tool_name) and tool_name in self.allowed_tools

    def require(self, tool_name: str) -> None:
        if not self.allows(tool_name):
            raise PermissionError(f"tool not allowed: {tool_name}")


@dataclass(frozen=True)
class AgentState:
    request: LegalResearchRequest
    candidate_authorities: tuple[LegalAuthority, ...]
    phase: AgentPhase = AgentPhase.COLLECT
    verified_authorities: tuple[VerifiedAuthority, ...] = ()
    answer: str | None = None
    failure: str | None = None


DraftAnswer = Callable[[AgentState], str]


class AgentWorkflow:
    """Fail-closed orchestration boundary for model-backed legal workflows.

    Model or graph runtimes may supply candidates and draft prose, but this
    class owns the deterministic transition into a citable/answerable state.
    No draft callback runs until at least one authority passes CitationFirewall.
    """

    def __init__(
        self,
        *,
        tool_policy: ToolPolicy,
        firewall: CitationFirewall | None = None,
    ) -> None:
        self.tool_policy = tool_policy
        self.firewall = firewall or CitationFirewall()

    def run(self, state: AgentState, *, draft_answer: DraftAnswer) -> AgentState:
        verifying = replace(state, phase=AgentPhase.VERIFY, answer=None, failure=None)
        try:
            research = ResearchWorkflow(self.firewall).evaluate(
                verifying.request,
                list(verifying.candidate_authorities),
            )
        except Exception:
            return replace(
                verifying,
                phase=AgentPhase.FAILED,
                verified_authorities=(),
                answer=None,
                failure="legal verification failed closed",
            )

        verified = research.citable_authorities
        if not verified:
            return replace(
                verifying,
                phase=AgentPhase.FAILED,
                verified_authorities=(),
                answer=None,
                failure="no verified legal authority available",
            )

        drafting = replace(
            verifying,
            phase=AgentPhase.DRAFT,
            verified_authorities=verified,
        )
        try:
            answer = draft_answer(drafting)
        except Exception:
            return replace(
                drafting,
                phase=AgentPhase.FAILED,
                answer=None,
                failure="model drafting failed closed",
            )

        normalized = answer.strip() if isinstance(answer, str) else ""
        if not normalized:
            return replace(
                drafting,
                phase=AgentPhase.FAILED,
                answer=None,
                failure="model returned no usable answer",
            )

        return replace(
            drafting,
            phase=AgentPhase.COMPLETE,
            answer=normalized,
            failure=None,
        )
