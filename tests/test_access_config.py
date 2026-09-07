import pytest

from nextlaw607.access import RejectingIdentityProvider
from nextlaw607.access_config import AccessConfigurationError, identity_provider_from_environment
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
