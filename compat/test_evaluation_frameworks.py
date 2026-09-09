def test_real_ragas_and_anthropic_packages_expose_required_interfaces():
    import anthropic
    import ragas
    from ragas.metrics import DiscreteMetric

    assert hasattr(ragas, "__version__")
    assert callable(DiscreteMetric)
    assert callable(anthropic.Anthropic)


def test_anthropic_client_can_initialize_without_network_call():
    import anthropic

    client = anthropic.Anthropic(api_key="test-key-not-used")
    assert hasattr(client, "messages")
    assert callable(client.messages.create)
