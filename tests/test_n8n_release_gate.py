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
    assert webhook["webhookId"] == "9e2322f8-7aed-4ad8-8d50-1dd620d52c0a"

    assert response["type"] == "n8n-nodes-base.respondToWebhook"
    body = response["parameters"]["responseBody"]
    assert '"scope":"development-only"' in body
    assert '"authority_eligible":false' in body
    assert '"trusted":false' in body
    assert '"verified_authority":false' in body

    serialized = json.dumps(workflow).lower()
    for forbidden in ("api_key", "authorization", "password", "private_key", "secret", "token"):
        assert forbidden not in serialized


def test_n8n_live_smoke_uses_static_webhook_path_and_proves_registration() -> None:
    workflow = json.loads(Path("config/n8n/release-smoke.json").read_text(encoding="utf-8"))
    webhook = next(node for node in workflow["nodes"] if node["name"] == "Release Smoke Webhook")
    assert ":" not in webhook["parameters"]["path"], "release smoke webhook must remain a static path"
    expected_route = f'/webhook/{webhook["parameters"]["path"]}'

    smoke = Path(".github/workflows/n8n-live-smoke.yml").read_text(encoding="utf-8")
    assert expected_route in smoke
    assert f'/webhook/{webhook["webhookId"]}/{webhook["parameters"]["path"]}' not in smoke
    assert 'webhook_entity' in smoke
    assert 'workflowId' in smoke
    assert 'nextlaw607ReleaseSmoke' in smoke


def test_n8n_live_smoke_activates_through_authenticated_runtime_api() -> None:
    smoke = Path(".github/workflows/n8n-live-smoke.yml").read_text(encoding="utf-8")

    assert "/rest/owner/setup" in smoke
    assert "/rest/login" in smoke
    assert "/rest/workflows/${workflow_id}/activate" in smoke
    assert '"versionId"' in smoke
    assert "import:workflow --input=/work/release-smoke.json --userId=\"$owner_id\"" in smoke
    assert "publish:workflow" not in smoke
    assert "curl -c \"$cookie_jar\"" in smoke
    assert "curl -b \"$cookie_jar\"" in smoke
