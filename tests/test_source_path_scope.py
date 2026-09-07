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
