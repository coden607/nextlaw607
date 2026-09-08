from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .stack_contract import validate_stack_manifest


@dataclass(frozen=True)
class ProductionReadiness:
    ready: bool
    blockers: tuple[str, ...]


def assess_production_readiness(manifest: Mapping[str, Any]) -> ProductionReadiness:
    """Fail closed until every required production-stack component is verified."""
    validate_stack_manifest(manifest)
    required = tuple(manifest["required_components"])
    components = manifest["components"]
    blockers = tuple(sorted(name for name in required if components[name]["status"] != "verified"))
    return ProductionReadiness(ready=not blockers, blockers=blockers)
