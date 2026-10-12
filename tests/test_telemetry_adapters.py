from contextlib import contextmanager

from nextlaw607.telemetry import (
    LangfuseSink,
    OpenTelemetrySink,
    PrivacySafeTelemetry,
    SentrySink,
)


class FakeSpan:
    def __init__(self):
        self.attributes = {}
        self.data = {}

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def set_data(self, key, value):
        self.data[key] = value


class FakeTracer:
    def __init__(self):
        self.names = []
        self.span = FakeSpan()

    @contextmanager
    def start_as_current_span(self, name):
        self.names.append(name)
        yield self.span


class FakeLangfuseObservation:
    def __init__(self):
        self.updates = []

    def update(self, **kwargs):
        self.updates.append(kwargs)


class FakeLangfuse:
    def __init__(self):
        self.calls = []
        self.observation = FakeLangfuseObservation()

    @contextmanager
    def start_as_current_observation(self, **kwargs):
        self.calls.append(kwargs)
        yield self.observation


class FakeSentry:
    def __init__(self):
        self.calls = []
        self.span = FakeSpan()

    @contextmanager
    def start_span(self, **kwargs):
        self.calls.append(kwargs)
        yield self.span


def test_opentelemetry_sink_receives_only_sanitized_attributes_and_correlation():
    tracer = FakeTracer()
    telemetry = PrivacySafeTelemetry(sinks=[OpenTelemetrySink(tracer=tracer)])
    telemetry.emit(
        name="agent.draft",
        correlation_id="req-607",
        attributes={"phase": "draft", "prompt": "private client prompt"},
    )

    assert tracer.names == ["agent.draft"]
    assert tracer.span.attributes["nextlaw.correlation_id"] == "req-607"
    assert tracer.span.attributes["nextlaw.phase"] == "draft"
    assert "private client prompt" not in repr(tracer.span.attributes)


def test_langfuse_sink_uses_safe_metadata_only():
    client = FakeLangfuse()
    telemetry = PrivacySafeTelemetry(sinks=[LangfuseSink(client=client)])
    telemetry.emit(
        name="llm.generation",
        correlation_id="trace-123",
        attributes={"model": "test-model", "authority_text": "private authority body"},
    )

    assert client.calls[0]["as_type"] == "span"
    assert client.calls[0]["name"] == "llm.generation"
    update = client.observation.updates[0]
    assert update["metadata"]["nextlaw.correlation_id"] == "trace-123"
    assert "private authority body" not in repr(update)


def test_sentry_sink_uses_safe_span_data_only():
    sentry = FakeSentry()
    telemetry = PrivacySafeTelemetry(sinks=[SentrySink(sentry=sentry)])
    telemetry.emit(
        name="request.error",
        correlation_id="error-1",
        attributes={"exception_type": "RuntimeError", "token": "secret-token-value"},
    )

    assert sentry.calls == [{"op": "nextlaw607.telemetry", "name": "request.error"}]
    assert sentry.span.data["nextlaw.correlation_id"] == "error-1"
    assert sentry.span.data["nextlaw.exception_type"] == "RuntimeError"
    assert "secret-token-value" not in repr(sentry.span.data)
