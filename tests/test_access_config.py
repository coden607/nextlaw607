import pytest

from nextlaw607.access import FreeEntitlementProvider, RejectingIdentityProvider
from nextlaw607.access_config import (
    AccessConfigurationError,
    entitlement_provider_from_environment,
    identity_provider_from_environment,
)
from nextlaw607.entitlement_store import RepositoryEntitlementProvider
from nextlaw607.supabase_identity import SupabaseIdentityProvider


def test_no_supabase_environment_keeps_rejecting_local_identity_provider():
    provider = identity_provider_from_environment({})
    assert isinstance(provider, RejectingIdentityProvider)


def test_complete_supabase_environment_enables_supabase_identity_provider():
    provider = identity_provider_from_environment({
        'SUPABASE_URL': 'https://example.supabase.co',
        'SUPABASE_PUBLISHABLE_KEY': 'sb_publishable_test',
    })
    assert isinstance(provider, SupabaseIdentityProvider)


def test_partial_supabase_environment_fails_closed():
    with pytest.raises(AccessConfigurationError, match='SUPABASE_URL.*SUPABASE_PUBLISHABLE_KEY'):
        identity_provider_from_environment({
            'SUPABASE_URL': 'https://example.supabase.co',
        })


def test_secret_supabase_key_is_rejected_by_environment_wiring():
    with pytest.raises(AccessConfigurationError, match='publishable key'):
        identity_provider_from_environment({
            'SUPABASE_URL': 'https://example.supabase.co',
            'SUPABASE_PUBLISHABLE_KEY': 'sb_secret_do_not_use_here',
        })


def test_no_secret_key_keeps_free_entitlement_provider():
    provider = entitlement_provider_from_environment({})
    assert isinstance(provider, FreeEntitlementProvider)


def test_complete_server_entitlement_environment_enables_repository_provider():
    provider = entitlement_provider_from_environment({
        'SUPABASE_URL': 'https://example.supabase.co',
        'SUPABASE_SECRET_KEY': 'sb_secret_backend_only',
    })
    assert isinstance(provider, RepositoryEntitlementProvider)


def test_secret_key_without_project_url_fails_closed():
    with pytest.raises(AccessConfigurationError, match='SUPABASE_URL.*SUPABASE_SECRET_KEY'):
        entitlement_provider_from_environment({
            'SUPABASE_SECRET_KEY': 'sb_secret_backend_only',
        })


def test_publishable_key_cannot_be_used_as_server_entitlement_secret():
    with pytest.raises(AccessConfigurationError, match='secret key'):
        entitlement_provider_from_environment({
            'SUPABASE_URL': 'https://example.supabase.co',
            'SUPABASE_SECRET_KEY': 'sb_publishable_not_allowed',
        })
