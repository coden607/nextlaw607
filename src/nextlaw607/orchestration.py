from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

_ALLOWED_ENGINES = {"archon", "n8n"}
_LEGAL_TRUST_FIELDS = {"authority_eligible", "trusted", "verified_authority"}
_SECRET_FIELD_FRAGMENTS = (
    "api_key",
    "apikey",
    "authorization",
    "password",
    "private_key",
    "secret",
    "token",
)


class OrchestrationPolicyError(ValueError):
    """Raised when development orchestration violates the trust boundary."""


@dataclass(frozen=True)
class DevelopmentTask:
    engine: str
    objective: str
    requested_tools: tuple[str, ...]
    payload: Mapping[str, Any]
    scope: str = "development-only"


def _contains_secret_like_field(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if any(fragment in normalized for fragment in _SECRET_FIELD_FRAGMENTS):
                return True
            if _contains_secret_like_field(nested):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_contains_secret_like_field(item) for item in value)
    return False


def _strip_legal_trust(value: Any) -> Any:
    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        for key, nested in value.items():
            normalized = str(key).strip().lower()
            cleaned[str(key)] = False if normalized in _LEGAL_TRUST_FIELDS else _strip_legal_trust(nested)
        for field in _LEGAL_TRUST_FIELDS:
            cleaned.setdefault(field, False)
        return cleaned
    if isinstance(value, list):
        return [_strip_legal_trust(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_strip_legal_trust(item) for item in value)
    return value


class DevelopmentOrchestrator:
    """Builds safe development-only task envelopes for Archon and n8n.

    This boundary does not execute provider workflows. It constrains what may be
    handed to a configured Archon/n8n runner and guarantees that orchestration
    metadata cannot promote content into legal authority.
    """

    def __init__(self, *, allowed_tools: Iterable[str]) -> None:
        self._allowed_tools = frozenset(tool for tool in allowed_tools if tool)

    def prepare_task(
        self,
        *,
        engine: str,
        objective: str,
        requested_tools: Iterable[str],
        payload: Mapping[str, Any],
    ) -> DevelopmentTask:
        normalized_engine = engine.strip().lower()
        if normalized_engine not in _ALLOWED_ENGINES:
            raise OrchestrationPolicyError("unsupported orchestration engine")
        if not objective.strip():
            raise OrchestrationPolicyError("objective is required")

        tools = tuple(requested_tools)
        if any(tool not in self._allowed_tools for tool in tools):
            raise OrchestrationPolicyError("tool is not allowlisted")
        if _contains_secret_like_field(payload):
            raise OrchestrationPolicyError("secret-like field is not allowed in orchestration payload")

        safe_payload = _strip_legal_trust(payload)
        return DevelopmentTask(
            engine=normalized_engine,
            objective=objective.strip(),
            requested_tools=tools,
            payload=MappingProxyType(safe_payload),
        )
