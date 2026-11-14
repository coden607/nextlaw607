from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class ProvisionKind(str, Enum):
    STATUTE = "statute"
    RULE = "rule"
    REGULATION = "regulation"


@dataclass(frozen=True)
class ProvisionVersion:
    entity_id: str
    kind: ProvisionKind
    jurisdiction: str
    citation: str
    title: str
    effective_from: date
    effective_to: date | None
    source_url: str
    content_sha256: str

    def __post_init__(self) -> None:
        for field_name in ("entity_id", "jurisdiction", "citation", "title", "source_url", "content_sha256"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} is required")
        if not self.source_url.startswith("https://"):
            raise ValueError("source_url must use https")
        if len(self.content_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in self.content_sha256):
            raise ValueError("content_sha256 must be a 64-character hex digest")
        if self.effective_to is not None and self.effective_to < self.effective_from:
            raise ValueError("effective_to cannot precede effective_from")

    def applies_on(self, on_date: date) -> bool:
        if on_date < self.effective_from:
            return False
        return self.effective_to is None or on_date <= self.effective_to


class CanonicalProvisionGraph:
    def __init__(self) -> None:
        self._versions: dict[str, list[ProvisionVersion]] = {}

    def add_version(self, version: ProvisionVersion) -> None:
        versions = self._versions.setdefault(version.entity_id, [])
        for existing in versions:
            if existing == version:
                return
            existing_end = existing.effective_to or date.max
            version_end = version.effective_to or date.max
            overlaps = not (version_end < existing.effective_from or existing_end < version.effective_from)
            if overlaps:
                raise ValueError("provision versions may not have overlapping effective ranges")
        versions.append(version)
        versions.sort(key=lambda item: item.effective_from)

    def resolve_on(self, entity_id: str, on_date: date) -> ProvisionVersion | None:
        candidates = [version for version in self._versions.get(entity_id, ()) if version.applies_on(on_date)]
        if len(candidates) > 1:
            raise RuntimeError("ambiguous provision version graph")
        return candidates[0] if candidates else None

    def lineage(self, entity_id: str) -> tuple[ProvisionVersion, ...]:
        return tuple(self._versions.get(entity_id, ()))
