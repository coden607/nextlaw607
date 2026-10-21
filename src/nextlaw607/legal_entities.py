from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class LegalEntityKind(str, Enum):
    CASE = "case"
    OPINION = "opinion"


@dataclass(frozen=True)
class CanonicalLegalEntity:
    entity_id: str
    kind: LegalEntityKind
    jurisdiction: str
    title: str
    court: str
    decision_date: date | None = None

    def __post_init__(self) -> None:
        for field_name in ("entity_id", "jurisdiction", "title", "court"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} is required")


@dataclass(frozen=True)
class CitationAlias:
    entity_id: str
    citation: str
    normalized_citation: str

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id is required")
        if not self.citation.strip() or not self.normalized_citation.strip():
            raise ValueError("citation and normalized_citation are required")


@dataclass(frozen=True)
class OpinionMembership:
    case_entity_id: str
    opinion_entity_id: str
    relationship: str = "opinion_of"

    def __post_init__(self) -> None:
        if not self.case_entity_id.strip() or not self.opinion_entity_id.strip():
            raise ValueError("case and opinion entity ids are required")
        if self.case_entity_id == self.opinion_entity_id:
            raise ValueError("case and opinion entity ids must differ")


class CanonicalCaseGraph:
    def __init__(self) -> None:
        self._entities: dict[str, CanonicalLegalEntity] = {}
        self._aliases: dict[str, str] = {}
        self._memberships: set[tuple[str, str]] = set()

    def add_entity(self, entity: CanonicalLegalEntity) -> None:
        existing = self._entities.get(entity.entity_id)
        if existing is not None and existing != entity:
            raise ValueError("entity_id collision")
        self._entities[entity.entity_id] = entity

    def add_alias(self, alias: CitationAlias) -> None:
        if alias.entity_id not in self._entities:
            raise ValueError("alias entity must exist")
        existing = self._aliases.get(alias.normalized_citation)
        if existing is not None and existing != alias.entity_id:
            raise ValueError("citation alias collision")
        self._aliases[alias.normalized_citation] = alias.entity_id

    def add_membership(self, membership: OpinionMembership) -> None:
        case = self._entities.get(membership.case_entity_id)
        opinion = self._entities.get(membership.opinion_entity_id)
        if case is None or opinion is None:
            raise ValueError("membership entities must exist")
        if case.kind is not LegalEntityKind.CASE or opinion.kind is not LegalEntityKind.OPINION:
            raise ValueError("membership must connect case to opinion")
        self._memberships.add((case.entity_id, opinion.entity_id))

    def resolve_citation(self, normalized_citation: str) -> CanonicalLegalEntity | None:
        entity_id = self._aliases.get(normalized_citation.strip())
        return self._entities.get(entity_id) if entity_id else None

    def opinions_for_case(self, case_entity_id: str) -> tuple[CanonicalLegalEntity, ...]:
        ids = sorted(opinion_id for case_id, opinion_id in self._memberships if case_id == case_entity_id)
        return tuple(self._entities[entity_id] for entity_id in ids)
