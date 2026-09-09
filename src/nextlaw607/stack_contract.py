from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

_ALLOWED_STATUSES = {"planned", "implemented", "configured", "verified", "evaluate"}


class StackContractError(ValueError):
    pass


@dataclass(frozen=True)
class StackContract:
    components: tuple[str, ...]


def validate_stack_manifest(manifest: Mapping[str, Any]) -> StackContract:
    if manifest.get("schema_version") != 1:
        raise StackContractError("schema_version must be 1")

    required = manifest.get("required_components")
    components = manifest.get("components")
    if not isinstance(required, list) or not all(isinstance(item, str) and item for item in required):
        raise StackContractError("required_components must be a list of names")
    if not isinstance(components, Mapping):
        raise StackContractError("components must be an object")

    missing = sorted(set(required) - set(components))
    if missing:
        raise StackContractError(f"required component missing: {', '.join(missing)}")

    for name, raw in components.items():
        if not isinstance(name, str) or not name or not isinstance(raw, Mapping):
            raise StackContractError("component entries must be named objects")
        status = raw.get("status")
        if status not in _ALLOWED_STATUSES:
            raise StackContractError(f"invalid status for {name}: {status!r}")
        implementation = raw.get("implementation", [])
        tests = raw.get("tests", [])
        evidence = raw.get("evidence", [])
        environment = raw.get("environment", [])
        for field_name, value in (
            ("implementation", implementation),
            ("tests", tests),
            ("evidence", evidence),
            ("environment", environment),
        ):
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise StackContractError(f"{name}.{field_name} must be a list of strings")
        if status in {"implemented", "configured", "verified"} and (not implementation or not tests):
            raise StackContractError(f"{status} component {name} requires implementation and tests")
        if status == "verified" and not evidence:
            raise StackContractError(f"verified component {name} requires evidence")

    return StackContract(components=tuple(sorted(components)))
