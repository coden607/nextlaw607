from __future__ import annotations

import json
from pathlib import Path


def test_n8n_release_workflow_is_development_only_and_cannot_promote_authority() -> None:
    workflow_path = Path("config/n8n/release-smoke.json")
    assert workflow_path.exists(), "n8n release smoke workflow must be committed"

    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    assert workflow["name"] == "NextLaw607 development-only release smoke"
    assert workflow["active"] is False

    nodes = {node["name"]: node for node in workflow["nodes"]}
    webhook = nodes["Release Smoke Webhook"]
    response = nodes["Return Safe Envelope"]

    assert webhook["type"] == "n8n-nodes-base.webhook"
    assert webhook["parameters"]["path"] == "nextlaw607-release-smoke"
    assert webhook["parameters"]["httpMethod"] == "POST"
    assert webhook["parameters"]["responseMode"] == "responseNode"

    assert response["type"] == "n8n-nodes-base.respondToWebhook"
    body = response["parameters"]["responseBody"]
    assert '"scope":"development-only"' in body
    assert '"authority_eligible":false' in body
    assert '"trusted":false' in body
    assert '"verified_authority":false' in body

    serialized = json.dumps(workflow).lower()
    for forbidden in ("api_key", "authorization", "password", "private_key", "secret", "token"):
        assert forbidden not in serialized
