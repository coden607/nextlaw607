from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SkillRecord:
    skill_id: str
    version: str
    source: str
    capabilities: frozenset[str]

    def __post_init__(self) -> None:
        if not self.skill_id.strip():
            raise ValueError("skill_id is required")
        if not self.version.strip():
            raise ValueError("version is required")
        if not self.source.startswith("https://github.com/coden607/skills"):
            raise ValueError("canonical skills must originate from coden607/skills")


class SkillRegistry:
    def __init__(self, records: Iterable[SkillRecord] = ()) -> None:
        self._records: dict[str, SkillRecord] = {}
        for record in records:
            self.register(record)

    def register(self, record: SkillRecord) -> None:
        existing = self._records.get(record.skill_id)
        if existing is not None and existing != record:
            raise ValueError(f"conflicting skill registration: {record.skill_id}")
        self._records[record.skill_id] = record

    def require(self, skill_id: str, capability: str | None = None) -> SkillRecord:
        try:
            record = self._records[skill_id]
        except KeyError as exc:
            raise KeyError(f"unknown skill: {skill_id}") from exc
        if capability is not None and capability not in record.capabilities:
            raise PermissionError(f"skill {skill_id} lacks capability {capability}")
        return record
