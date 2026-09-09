from __future__ import annotations

import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

import sentry_sdk

from nextlaw607.telemetry import PrivacySafeTelemetry, SentrySink


RAW_PROMPT = "private client prompt"
RAW_EMAIL = "client@example.com"
REDACTED = "[REDACTED]"


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise AssertionError(f"{name} is required for the controlled Sentry live smoke")
    return value


def _read_event(*, base_url: str, org: str, project: str, event_id: str, token: str) -> dict:
    endpoint = (
        f"{base_url.rstrip('/')}/api/0/projects/{quote(org, safe='')}/"
        f"{quote(project, safe='')}/events/{quote(event_id, safe='')}/"
    )
    request = Request(
        endpoint,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def test_sentry_live_export_is_sanitized_and_revision_bound():
    revision = _required("NEXTLAW_EXACT_REVISION")
    dsn = _required("SENTRY_DSN")
    token = _required("SENTRY_AUTH_TOKEN")
    org = _required("SENTRY_ORG")
    project = _required("SENTRY_PROJECT")
    base_url = os.environ.get("SENTRY_BASE_URL", "https://sentry.io").strip().rstrip("/")
    assert base_url.startswith("https://"), "SENTRY_BASE_URL must use HTTPS"

    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0,
        send_default_pii=False,
        environment="nextlaw607-release-smoke",
        release=revision,
    )

    telemetry = PrivacySafeTelemetry(sinks=(SentrySink(sentry=sentry_sdk),))
    event = telemetry.emit(
        name="nextlaw607.sentry.release-smoke",
        correlation_id=f"sentry-{revision[:12]}",
        attributes={
            "prompt": RAW_PROMPT,
            "contact": RAW_EMAIL,
            "authority_eligible": False,
            "revision": revision,
        },
    )

    assert event.attributes["prompt"] == REDACTED
    assert event.attributes["contact"] == REDACTED
    assert event.attributes["authority_eligible"] is False
    assert telemetry.sink_failures == 0

    marker = f"nextlaw607-sentry-release-{revision[:16]}"
    with sentry_sdk.push_scope() as scope:
        scope.set_tag("nextlaw.release_revision", revision)
        scope.set_tag("nextlaw.authority_eligible", "false")
        scope.set_extra("nextlaw.correlation_id", event.correlation_id)
        scope.set_extra("nextlaw.attributes", dict(event.attributes))
        event_id = sentry_sdk.capture_message(marker, level="info")

    assert event_id is not None, "Sentry did not accept the release-smoke event"
    assert sentry_sdk.flush(timeout=10), "Sentry transport did not flush successfully"

    provider_event = None
    last_error: Exception | None = None
    for _ in range(12):
        try:
            provider_event = _read_event(
                base_url=base_url,
                org=org,
                project=project,
                event_id=str(event_id),
                token=token,
            )
            break
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {404, 429}:
                raise
        time.sleep(5)

    if provider_event is None:
        raise AssertionError(f"Sentry provider readback did not become visible: {last_error!r}")

    serialized = json.dumps(provider_event, sort_keys=True)
    assert marker in serialized
    assert revision in serialized
    assert RAW_PROMPT not in serialized
    assert RAW_EMAIL not in serialized
    assert REDACTED in serialized
    assert "authority_eligible" in serialized

    Path("sentry-live-evidence.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "revision": revision,
                "provider": "sentry",
                "event_id": str(event_id),
                "privacy_boundary": "PrivacySafeTelemetry->SentrySink",
                "authority_eligible": False,
                "raw_prompt_absent": True,
                "raw_email_absent": True,
                "provider_readback": "passed",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
