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


def test_registered_legal_sources_require_https_transport():
    registry = SourceRegistry()
    insecure = "http://www.nycourts.gov/reporter/3dseries/2024/example.htm"

    assert not registry.is_registered_url(insecure)
    assert not registry.is_official_url(insecure, "NY")
    assert not registry.supports(insecure, "primary_text", "NY")
    assert registry.provider_identity(insecure, "NY") is None
