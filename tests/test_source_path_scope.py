from nextlaw607.sources import SourceCapability, SourceRegistry


def test_registered_source_with_path_scope_rejects_same_host_outside_scope():
    registry = SourceRegistry()
    unrelated = "https://govt.westlaw.com/nylaw/document/example"

    assert registry.is_registered_url(unrelated) is False
    assert registry.provider_identity(unrelated, "NY") is None
    assert registry.supports(unrelated, SourceCapability.PRIMARY_TEXT, "NY") is False


def test_registered_source_with_path_scope_accepts_path_and_descendants():
    registry = SourceRegistry()

    root = "https://govt.westlaw.com/nycrr"
    descendant = "https://govt.westlaw.com/nycrr/Document/example"

    assert registry.is_registered_url(root) is True
    assert registry.is_registered_url(descendant) is True
    assert registry.supports(descendant, SourceCapability.PRIMARY_TEXT, "NY") is True


def test_registered_source_rejects_unregistered_subdomain_of_trusted_domain():
    registry = SourceRegistry()
    unregistered_subdomain = "https://attacker.nycourts.gov/opinion/example"

    assert registry.is_registered_url(unregistered_subdomain) is False
    assert registry.is_official_url(unregistered_subdomain, "NY") is False
    assert registry.provider_identity(unregistered_subdomain, "NY") is None
    assert registry.supports(unregistered_subdomain, SourceCapability.PRIMARY_TEXT, "NY") is False


def test_registered_source_rejects_embedded_url_credentials():
    registry = SourceRegistry()
    credential_bearing = "https://user:secret@www.nycourts.gov/opinion/example"

    assert registry.is_registered_url(credential_bearing) is False
    assert registry.is_official_url(credential_bearing, "NY") is False
    assert registry.provider_identity(credential_bearing, "NY") is None
    assert registry.supports(credential_bearing, SourceCapability.PRIMARY_TEXT, "NY") is False
