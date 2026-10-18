import pytest

from nextlaw607.skill_registry import SkillRecord, SkillRegistry


SOURCE = "https://github.com/coden607/skills/tree/main/legal-war-room"


def test_registry_requires_canonical_provenance():
    registry = SkillRegistry(
        [SkillRecord("legal-war-room", "1", SOURCE, frozenset({"legal-analysis"}))]
    )
    assert registry.require("legal-war-room", "legal-analysis").skill_id == "legal-war-room"


def test_registry_rejects_noncanonical_source():
    with pytest.raises(ValueError):
        SkillRecord("bad", "1", "https://example.com/skills/bad", frozenset())


def test_registry_rejects_capability_mismatch():
    registry = SkillRegistry(
        [SkillRecord("legal-war-room", "1", SOURCE, frozenset({"legal-analysis"}))]
    )
    with pytest.raises(PermissionError):
        registry.require("legal-war-room", "destructive-write")
