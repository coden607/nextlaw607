from nextlaw607.telemetry import PrivacySafeTelemetry, TelemetryEvent


def test_telemetry_release_gate_redacts_correlation_identifier_before_any_sink():
    captured: list[TelemetryEvent] = []
    telemetry = PrivacySafeTelemetry(sinks=[captured.append])

    event = telemetry.emit(
        name="legal.verify",
        correlation_id="client@example.com Bearer sk-live-secret-token 123-45-6789",
        attributes={"phase": "verify"},
    )

    rendered = repr(event)
    assert "client@example.com" not in rendered
    assert "sk-live-secret-token" not in rendered
    assert "123-45-6789" not in rendered
    assert captured == [event]
