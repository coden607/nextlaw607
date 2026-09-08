from nextlaw607.telemetry import (
    LangfuseSink,
    OpenTelemetrySink,
    PrivacySafeTelemetry,
    SentrySink,
)


def test_real_opentelemetry_sdk_records_only_sanitized_attributes():
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("nextlaw607.compat")

    telemetry = PrivacySafeTelemetry(sinks=[OpenTelemetrySink(tracer=tracer)])
    telemetry.emit(
        name="compat.otel",
        correlation_id="compat-607",
        attributes={"phase": "verify", "prompt": "private facts must never export"},
    )

    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    attrs = dict(spans[0].attributes)
    assert attrs["nextlaw.correlation_id"] == "compat-607"
    assert attrs["nextlaw.phase"] == "verify"
    assert "private facts" not in repr(attrs)


def test_real_langfuse_v4_client_can_be_used_with_tracing_disabled():
    from langfuse import Langfuse

    client = Langfuse(tracing_enabled=False)
    telemetry = PrivacySafeTelemetry(sinks=[LangfuseSink(client=client)])
    event = telemetry.emit(
        name="compat.langfuse",
        correlation_id="compat-langfuse",
        attributes={"model": "offline-test", "authority_text": "private authority body"},
    )

    assert telemetry.sink_failures == 0
    assert event.attributes["authority_text"] == "[REDACTED]"


def test_real_sentry_sdk_can_create_local_unsampled_span_without_pii():
    import sentry_sdk

    sentry_sdk.init(dsn=None, traces_sample_rate=0.0, send_default_pii=False)
    telemetry = PrivacySafeTelemetry(sinks=[SentrySink(sentry=sentry_sdk)])
    event = telemetry.emit(
        name="compat.sentry",
        correlation_id="compat-sentry",
        attributes={"exception_type": "RuntimeError", "token": "secret-token-value"},
    )

    assert telemetry.sink_failures == 0
    assert event.attributes["token"] == "[REDACTED]"
