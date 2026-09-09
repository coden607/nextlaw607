from nextlaw607.telemetry import (
    PrivacySafeTelemetry,
    TelemetryEvent,
    redact_telemetry_value,
)


def test_recursive_telemetry_redaction_removes_secrets_and_private_legal_content():
    payload = {
        "authorization": "Bearer sk-live-secret-token",
        "api_key": "super-secret-key",
        "case_private_content": "client confession and private strategy",
        "legal_source_text": "full private legal work product",
        "nested": {
            "email": "person@example.com",
            "safe_count": 7,
        },
    }

    redacted = redact_telemetry_value(payload)

    rendered = repr(redacted)
    assert "sk-live-secret-token" not in rendered
    assert "super-secret-key" not in rendered
    assert "client confession" not in rendered
    assert "private legal work product" not in rendered
    assert "person@example.com" not in rendered
    assert redacted["nested"]["safe_count"] == 7


def test_telemetry_correlation_is_retained_without_raw_prompt_or_authority_text():
    captured: list[TelemetryEvent] = []
    telemetry = PrivacySafeTelemetry(sinks=[captured.append])

    event = telemetry.emit(
        name="agent.verify",
        correlation_id="req-607",
        attributes={
            "phase": "verify",
            "prompt": "private client facts that must not leave the trust boundary",
            "authority_text": "full opinion text should not be copied to telemetry",
            "verified_authority_count": 2,
        },
    )

    assert event.correlation_id == "req-607"
    assert captured == [event]
    assert event.attributes["phase"] == "verify"
    assert event.attributes["verified_authority_count"] == 2
    assert "private client facts" not in repr(event.attributes)
    assert "full opinion text" not in repr(event.attributes)


def test_sink_failures_never_break_legal_workflow_or_leak_unsanitized_payload():
    seen = []

    def failing_sink(event: TelemetryEvent) -> None:
        seen.append(event)
        raise RuntimeError("telemetry backend unavailable")

    telemetry = PrivacySafeTelemetry(sinks=[failing_sink])
    event = telemetry.emit(
        name="legal.research",
        correlation_id="case-123",
        attributes={"token": "secret-token-value", "result": "ok"},
    )

    assert event.attributes["result"] == "ok"
    assert "secret-token-value" not in repr(seen[0])
    assert telemetry.sink_failures == 1
