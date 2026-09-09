from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from nextlaw607.telemetry import OpenTelemetrySink, PrivacySafeTelemetry


class _CaptureHandler(BaseHTTPRequestHandler):
    payloads: list[bytes] = []

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        length = int(self.headers.get("Content-Length", "0"))
        self.__class__.payloads.append(self.rfile.read(length))
        self.send_response(200)
        self.send_header("Content-Type", "application/x-protobuf")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def _collect_attributes(request: ExportTraceServiceRequest) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for resource_spans in request.resource_spans:
        for scope_spans in resource_spans.scope_spans:
            for span in scope_spans.spans:
                for attribute in span.attributes:
                    value = attribute.value
                    if value.HasField("string_value"):
                        attributes[attribute.key] = value.string_value
                    elif value.HasField("int_value"):
                        attributes[attribute.key] = str(value.int_value)
                    elif value.HasField("bool_value"):
                        attributes[attribute.key] = str(value.bool_value)
    return attributes


def test_real_otlp_http_export_contains_only_sanitized_nextlaw_metadata():
    _CaptureHandler.payloads = []
    server = HTTPServer(("127.0.0.1", 0), _CaptureHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=f"http://127.0.0.1:{server.server_port}/v1/traces")
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("nextlaw607-live-smoke")

    telemetry = PrivacySafeTelemetry(sinks=[OpenTelemetrySink(tracer=tracer)])
    telemetry.emit(
        name="legal.verify",
        correlation_id="client@example.com Bearer sk-live-secret-token 123-45-6789",
        attributes={
            "phase": "verify",
            "prompt": "private client prompt",
            "token": "secret-token-value",
            "verified_authority_count": 2,
        },
    )
    provider.force_flush()
    provider.shutdown()
    server.shutdown()
    thread.join(timeout=5)

    assert _CaptureHandler.payloads, "OTLP receiver did not receive any trace export"
    body = b"".join(_CaptureHandler.payloads)
    assert b"client@example.com" not in body
    assert b"sk-live-secret-token" not in body
    assert b"123-45-6789" not in body
    assert b"private client prompt" not in body
    assert b"secret-token-value" not in body

    request = ExportTraceServiceRequest()
    request.ParseFromString(_CaptureHandler.payloads[-1])
    attributes = _collect_attributes(request)
    assert attributes["nextlaw.phase"] == "verify"
    assert attributes["nextlaw.verified_authority_count"] == "2"
    assert attributes["nextlaw.correlation_id"] == "[REDACTED] [REDACTED] [REDACTED]"
