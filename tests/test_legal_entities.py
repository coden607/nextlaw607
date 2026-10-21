from datetime import date

import pytest

from nextlaw607.legal_entities import (
    CanonicalCaseGraph,
    CanonicalLegalEntity,
    CitationAlias,
    LegalEntityKind,
    OpinionMembership,
)


def test_case_graph_resolves_parallel_aliases_and_opinions():
    graph = CanonicalCaseGraph()
    case = CanonicalLegalEntity(
        entity_id="case:people-v-example",
        kind=LegalEntityKind.CASE,
        jurisdiction="NY",
        title="People v Example",
        court="NY Court of Appeals",
        decision_date=date(2026, 1, 1),
    )
    opinion = CanonicalLegalEntity(
        entity_id="opinion:people-v-example:majority",
        kind=LegalEntityKind.OPINION,
        jurisdiction="NY",
        title="People v Example — majority",
        court="NY Court of Appeals",
        decision_date=date(2026, 1, 1),
    )
    graph.add_entity(case)
    graph.add_entity(opinion)
    graph.add_membership(OpinionMembership(case.entity_id, opinion.entity_id))
    graph.add_alias(CitationAlias(case.entity_id, "1 N.Y.3d 1", "1 ny3d 1"))
    graph.add_alias(CitationAlias(case.entity_id, "2026 NY Slip Op 00001", "2026 ny slip op 00001"))

    assert graph.resolve_citation("1 ny3d 1") == case
    assert graph.resolve_citation("2026 ny slip op 00001") == case
    assert graph.opinions_for_case(case.entity_id) == (opinion,)


def test_case_graph_fails_closed_on_collisions_or_invalid_membership():
    graph = CanonicalCaseGraph()
    case = CanonicalLegalEntity("case:a", LegalEntityKind.CASE, "NY", "A", "Court")
    other = CanonicalLegalEntity("case:b", LegalEntityKind.CASE, "NY", "B", "Court")
    graph.add_entity(case)
    graph.add_entity(other)
    graph.add_alias(CitationAlias(case.entity_id, "1 A 1", "1 a 1"))

    with pytest.raises(ValueError, match="collision"):
        graph.add_alias(CitationAlias(other.entity_id, "1 A 1", "1 a 1"))
    with pytest.raises(ValueError, match="case to opinion"):
        graph.add_membership(OpinionMembership(case.entity_id, other.entity_id))
