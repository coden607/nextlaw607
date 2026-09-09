from __future__ import annotations

import json
from pathlib import Path

from nextlaw607.release_readiness import assess_production_readiness


def _manifest() -> dict:
    return json.loads(Path("config/production-stack.json").read_text(encoding="utf-8"))


def test_production_readiness_fails_closed_until_every_required_component_is_verified() -> None:
    result = assess_production_readiness(_manifest())

    assert result.ready is False
    assert "cloudflare" in result.blockers
    assert "mem0" in result.blockers
    assert "citation-firewall" not in result.blockers
    assert "docker" not in result.blockers
    assert "pgvector" not in result.blockers


def test_production_readiness_passes_only_when_all_required_components_are_verified() -> None:
    manifest = _manifest()
    for name in manifest["required_components"]:
        manifest["components"][name]["status"] = "verified"
        manifest["components"][name].setdefault("evidence", ["controlled-test-evidence"])
        if not manifest["components"][name]["evidence"]:
            manifest["components"][name]["evidence"] = ["controlled-test-evidence"]

    result = assess_production_readiness(manifest)

    assert result.ready is True
    assert result.blockers == ()
