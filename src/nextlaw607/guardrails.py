from __future__ import annotations

from dataclasses import dataclass
import re
from collections.abc import Iterable


@dataclass(frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str


class GuardrailGate:
    """Deterministic safety boundary that runs before any model or tool call.

    This gate does not determine legal authority. CitationFirewall remains the only
    component allowed to promote legal material to verified authority.
    """

    _INJECTION_PATTERNS = (
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
        re.compile(r"bypass\s+citationfirewall", re.I),
        re.compile(r"mark\s+.*\s+verified", re.I),
        re.compile(r"disable\s+(the\s+)?guardrails?", re.I),
    )
    _SECRET_PATTERNS = (
        re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
        re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{8,}\b", re.I),
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    )

    def inspect_input(self, text: str) -> GuardrailDecision:
        if not isinstance(text, str) or not text.strip():
            return GuardrailDecision(False, "empty or invalid input")
        for pattern in self._INJECTION_PATTERNS:
            if pattern.search(text):
                return GuardrailDecision(False, "prompt injection or CitationFirewall bypass attempt")
        return GuardrailDecision(True, "input allowed")

    def redact_sensitive(self, text: str) -> str:
        redacted = text
        for pattern in self._SECRET_PATTERNS:
            redacted = pattern.sub("[REDACTED:SENSITIVE]", redacted)
        return redacted


class ToolAuthorizer:
    """Explicit allowlist with default deny and a non-overridable legal trust boundary."""

    _TOOL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")

    def __init__(self, *, allowed_tools: Iterable[str] = ()) -> None:
        self._allowed_tools = frozenset(str(tool).strip() for tool in allowed_tools if str(tool).strip())

    def authorize(self, tool_name: str, *, attempts_authority_promotion: bool = False) -> GuardrailDecision:
        if attempts_authority_promotion:
            return GuardrailDecision(False, "CitationFirewall cannot be overridden by tool authorization")
        if not isinstance(tool_name, str) or not self._TOOL_NAME_PATTERN.fullmatch(tool_name):
            return GuardrailDecision(False, "invalid tool identifier")
        if tool_name not in self._allowed_tools:
            return GuardrailDecision(False, "tool is not on the explicit allowlist")
        return GuardrailDecision(True, "tool allowed")


class NemoGuardrailsAdapter:
    """Optional NeMo runtime bridge behind NextLaw's deterministic gate.

    NeMo can add programmable rails, but it never replaces deterministic input
    checks, tool authorization, or CitationFirewall legal verification.
    """

    def __init__(self, *, gate: GuardrailGate | None = None) -> None:
        self.gate = gate or GuardrailGate()

    def preflight(self, text: str) -> GuardrailDecision:
        return self.gate.inspect_input(text)

    def runtime_status(self) -> GuardrailDecision:
        try:
            from nemoguardrails import RailsConfig  # noqa: F401
        except Exception:
            return GuardrailDecision(False, "NeMo Guardrails runtime unavailable")
        return GuardrailDecision(True, "NeMo Guardrails runtime available")
