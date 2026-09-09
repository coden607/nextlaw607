from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from nextlaw607.telemetry import PrivacySafeTelemetry, SentrySink


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required provider configuration: {name}")
    return value


def test_sentry_live_export_and_provider_readback():
    import sentry_sdk

    dsn = _required("SENTRY_DSN")
    auth_token = _required("SENTRY_AUTH_TOKEN")
    org = _required("SENTRY_ORG")
    project = _required("SENTRY_PROJECT")
    revision = _required("NEXTLAW_EXACT_REVISION")

    sentry_sdk.init(dsn=dsn, send_default_pii=False, traces_sample_rate=0.0)
    telemetry = PrivacySafeTelemetry((SentrySink(sentry=sentry_sdk),))
    telemetry.emit(
        name="nextlaw607.sentry.live-smoke",
        correlation_id=f"provider-smoke-{revision[:12]}",
        attributes={
            "authority_eligible": False,
            "revision": revision,
            "prompt": "private client prompt",
            "contact": "client@example.com",
        },
    )

    sentry_sdk.set_tag("nextlaw_exact_revision", revision)
    sentry_sdk.set_tag("authority_eligible", "false")
    event_id = sentry_sdk.capture_message("nextlaw607 provider verification smoke", level="info")
    sentry_sdk.flush(timeout=10)
    assert event_id, "Sentry did not return an event id"

    url = f"https://sentry.io/api/0/projects/{org}/{project}/events/{event_id}/"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json",
            "User-Agent": "nextlaw607-provider-verification",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)

    returned_id = str(payload.get("eventID") or payload.get("event_id") or payload.get("id") or "")
    assert returned_id.replace("-", "").lower() == str(event_id).replace("-", "").lower()

    Path("sentry-live-evidence.json").write_text(
        json.dumps(
            {
                "provider": "sentry",
                "revision": revision,
                "event_id": str(event_id),
                "provider_readback": True,
                "authority_eligible": False,
            },
            sort_keys=True,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
