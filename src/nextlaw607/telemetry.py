from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Mapping, Sequence

_REDACTED = "[REDACTED]"
_SENSITIVE_KEYS = {
    "authorization",
    "api_key",
    "apikey",
    "secret",
    "secret_key",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "prompt",
    "raw_prompt",
    "case_private_content",
    "private_content",
    "legal_source_text",
    "authority_text",
    "work_product",
}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9._~+\-/=]+", re.IGNORECASE)
_API_SECRET_RE = re.compile(r"\b(?:sk|sb_secret|api)[-_][A-Za-z0-9._~+\-/=]{8,}\b", re.IGNORECASE)
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def _redact_string(value: str) -> str:
    value = _BEARER_RE.sub(_REDACTED, value)
    value = _API_SECRET_RE.sub(_REDACTED, value)
    value = _EMAIL_RE.sub(_REDACTED, value)
    value = _SSN_RE.sub(_REDACTED, value)
    return value


def redact_telemetry_value(value: Any, *, key: str | None = None) -> Any:
    if key is not None and key.lower() in _SENSITIVE_KEYS:
        return _REDACTED
    if isinstance(value, Mapping):
        return {
            str(item_key): redact_telemetry_value(item_value, key=str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, tuple):
        return tuple(redact_telemetry_value(item) for item in value)
    if isinstance(value, list):
        return [redact_telemetry_value(item) for item in value]
    if isinstance(value, set):
        return {redact_telemetry_value(item) for item in value}
    if isinstance(value, str):
        return _redact_string(value)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return _redact_string(str(value))


@dataclass(frozen=True)
class TelemetryEvent:
    name: str
    correlation_id: str
    attributes: Mapping[str, Any]


TelemetrySink = Callable[[TelemetryEvent], None]


class PrivacySafeTelemetry:
    """Fail-open observability with fail-closed payload privacy.

    Telemetry failures must never alter legal workflow behavior. All data is
    sanitized before any sink sees it, and only the correlation identifier is
    retained verbatim so traces can be joined without copying private content.
    """

    def __init__(self, sinks: Sequence[TelemetrySink] = ()) -> None:
        self._sinks = tuple(sinks)
        self.sink_failures = 0

    def emit(
        self,
        *,
        name: str,
        correlation_id: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> TelemetryEvent:
        event = TelemetryEvent(
            name=_redact_string(str(name)),
            correlation_id=str(correlation_id),
            attributes=redact_telemetry_value(dict(attributes or {})),
        )
        for sink in self._sinks:
            try:
                sink(event)
            except Exception:
                self.sink_failures += 1
        return event
