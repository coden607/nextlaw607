from nextlaw607.sources import SourceRegistry


def test_ny_verification_accepts_binding_federal_official_sources():
    registry = SourceRegistry()

    assert registry.is_official_url(
        "https://www.supremecourt.gov/opinions/23pdf/22-915_8o6b.pdf",
        "NY",
    )
    assert registry.supports(
        "https://www.ca2.uscourts.gov/decisions/isysquery/example.pdf",
        "primary_text",
        "NY",
    )


def test_us_scope_does_not_treat_state_only_sources_as_federal_sources():
    registry = SourceRegistry()

    assert not registry.is_official_url(
        "https://www.nycourts.gov/reporter/3dseries/2024/example.htm",
        "US",
    )
