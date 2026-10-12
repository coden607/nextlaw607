from __future__ import annotations

import json
import os
from pathlib import Path
import time
from typing import Any

from langfuse import get_client

from nextlaw607.telemetry import LangfuseSink, PrivacySafeTelemetry


PRIVATE_PROMPT = "private client prompt"
PRIVATE_EMAIL = "client@example.com"
EVIDENCE_PATH = Path("langfuse-live-evidence.json")


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "__dict__"):
        return {
            str(key): _jsonable(item)
            for key, item in vars(value).items()
            if not str(key).startswith("_")
        }
    return value


def _observations(response: Any) -> list[Any]:
    data = getattr(response, "data", response)
    if isinstance(data, list):
        return data
    if isinstance(data, tuple):
        return list(data)
    return []


def test_langfuse_provider_receives_only_sanitized_nextlaw_metadata():
    revision = os.environ["NEXTLAW_EXACT_REVISION"]
    assert len(revision) == 40

    client = get_client()
    trace_id = client.create_trace_id(seed=f"nextlaw607:{revision}:langfuse-live")
    telemetry = PrivacySafeTelemetry(sinks=[LangfuseSink(client=client)])

    with client.start_as_current_observation(
        as_type="span",
        name="nextlaw607.langfuse.live.root",
        trace_context={"trace_id": trace_id},
    ):
        event = telemetry.emit(
            name="nextlaw607.langfuse.live",
            correlation_id=f"release-{revision[:12]}",
            attributes={
                "phase": "release-evidence",
                "prompt": PRIVATE_PROMPT,
                "contact": PRIVATE_EMAIL,
                "authority_eligible": False,
            },
        )

    assert event.attributes["prompt"] == "[REDACTED]"
    assert event.attributes["contact"] == "[REDACTED]"
    assert event.attributes["authority_eligible"] is False

    client.flush()

    found = None
    deadline = time.monotonic() + 75
    while time.monotonic() < deadline:
        response = client.api.observations.get_many(trace_id=trace_id)
        for observation in _observations(response):
            if getattr(observation, "name", None) == "nextlaw607.langfuse.live":
                found = observation
                break
        if found is not None:
            break
        time.sleep(2)

    assert found is not None, "Langfuse observation did not become readable before deadline"
    payload = _jsonable(found)
    serialized = json.dumps(payload, sort_keys=True, default=str)

    assert PRIVATE_PROMPT not in serialized
    assert PRIVATE_EMAIL not in serialized
    assert "[REDACTED]" in serialized
    assert "authority_eligible" in serialized
    assert "false" in serialized.lower()

    EVIDENCE_PATH.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "revision": revision,
                "provider": "langfuse",
                "trace_id": trace_id,
                "server_readback": "passed",
                "sensitive_canaries_absent": True,
                "authority_eligible": False,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    client.shutdown()
