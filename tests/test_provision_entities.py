from datetime import date

import pytest

from nextlaw607.provision_entities import CanonicalProvisionGraph, ProvisionKind, ProvisionVersion


def _version(start, end, digest):
    return ProvisionVersion(
        entity_id="ny:cpl:245.20",
        kind=ProvisionKind.STATUTE,
        jurisdiction="NY",
        citation="CPL 245.20",
        title="Automatic discovery",
        effective_from=start,
        effective_to=end,
        source_url="https://legislation.nysenate.gov/example",
        content_sha256=digest,
    )


def test_provision_graph_resolves_historical_version_by_effective_date():
    graph = CanonicalProvisionGraph()
    old = _version(date(2024, 1, 1), date(2025, 12, 31), "a" * 64)
    current = _version(date(2026, 1, 1), None, "b" * 64)
    graph.add_version(old)
    graph.add_version(current)

    assert graph.resolve_on("ny:cpl:245.20", date(2025, 6, 1)) == old
    assert graph.resolve_on("ny:cpl:245.20", date(2026, 10, 21)) == current
    assert graph.lineage("ny:cpl:245.20") == (old, current)


def test_provision_graph_rejects_overlapping_versions():
    graph = CanonicalProvisionGraph()
    graph.add_version(_version(date(2024, 1, 1), date(2025, 12, 31), "a" * 64))
    with pytest.raises(ValueError, match="overlapping"):
        graph.add_version(_version(date(2025, 1, 1), None, "b" * 64))


def test_provision_version_requires_https_hash_and_valid_range():
    with pytest.raises(ValueError, match="https"):
        ProvisionVersion("x", ProvisionKind.RULE, "NY", "R", "Rule", date(2026, 1, 1), None, "http://x", "a" * 64)
    with pytest.raises(ValueError, match="64-character"):
        ProvisionVersion("x", ProvisionKind.RULE, "NY", "R", "Rule", date(2026, 1, 1), None, "https://x", "bad")
    with pytest.raises(ValueError, match="effective_to"):
        ProvisionVersion("x", ProvisionKind.RULE, "NY", "R", "Rule", date(2026, 1, 2), date(2026, 1, 1), "https://x", "a" * 64)
