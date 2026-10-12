import json
from pathlib import Path

import pytest

from nextlaw607.stack_contract import StackContractError, validate_stack_manifest


REQUIRED_COMPONENTS = {
    "supabase",
    "postgres",
    "pgvector",
    "pydantic-ai",
    "langgraph",
    "archon",
    "n8n",
    "docling",
    "crawl4ai",
    "mem0",
    "nemo-guardrails",
    "tool-authorization",
    "langfuse",
    "opentelemetry",
    "sentry",
    "ragas",
    "playwright",
    "claude-evaluator",
    "cloudflare",
    "docker",
    "github-actions",
    "citation-firewall",
}


def test_committed_manifest_covers_every_approved_component():
    manifest = json.loads(Path("config/production-stack.json").read_text(encoding="utf-8"))
    result = validate_stack_manifest(manifest)
    assert REQUIRED_COMPONENTS <= set(result.components)


def test_required_component_cannot_be_omitted():
    with pytest.raises(StackContractError, match="required component"):
        validate_stack_manifest({
            "schema_version": 1,
            "required_components": ["supabase"],
            "components": {},
        })


def test_verified_component_requires_implementation_and_evidence():
    with pytest.raises(StackContractError, match="verified"):
        validate_stack_manifest({
            "schema_version": 1,
            "required_components": ["supabase"],
            "components": {
                "supabase": {
                    "status": "verified",
                    "implementation": [],
                    "tests": [],
                    "evidence": [],
                    "environment": [],
                }
            },
        })


def test_manifest_rejects_unknown_lifecycle_status():
    with pytest.raises(StackContractError, match="status"):
        validate_stack_manifest({
            "schema_version": 1,
            "required_components": ["supabase"],
            "components": {
                "supabase": {
                    "status": "magic",
                    "implementation": ["src/example.py"],
                    "tests": ["tests/test_example.py"],
                    "evidence": [],
                    "environment": [],
                }
            },
        })
