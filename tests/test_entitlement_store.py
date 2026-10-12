from nextlaw607.access import FOUNDER_ENTITLEMENT, FREE_ENTITLEMENT, VerifiedIdentity
from nextlaw607.entitlement_store import RepositoryEntitlementProvider


def test_missing_authoritative_entitlement_defaults_to_free():
    provider = RepositoryEntitlementProvider(lambda subject: None)
    assert provider.entitlement_for(VerifiedIdentity('user-1', 'supabase')) == FREE_ENTITLEMENT


def test_authoritative_paid_entitlement_is_loaded_for_verified_subject():
    seen = []

    def lookup(subject: str):
        seen.append(subject)
        return {
            'tier': 'premium',
            'source': 'purchase',
            'expires_at': '2027-01-01T00:00:00+00:00',
            'revocable': True,
            'billing_required': True,
        }

    provider = RepositoryEntitlementProvider(lookup)
    entitlement = provider.entitlement_for(VerifiedIdentity('user-123', 'supabase'))

    assert seen == ['user-123']
    assert entitlement.tier == 'premium'
    assert entitlement.source == 'purchase'
    assert entitlement.billing_required is True


def test_founder_source_is_canonicalized_to_immutable_lifetime_grant():
    provider = RepositoryEntitlementProvider(lambda subject: {
        'tier': 'free',
        'source': 'founder_lifetime_grant',
        'expires_at': '2026-01-01T00:00:00+00:00',
        'revocable': True,
        'billing_required': True,
    })
    entitlement = provider.entitlement_for(VerifiedIdentity('founder-1', 'supabase'))
    assert entitlement == FOUNDER_ENTITLEMENT


def test_malformed_authoritative_entitlement_fails_closed_to_free():
    provider = RepositoryEntitlementProvider(lambda subject: {
        'tier': 'super_admin_forever',
        'source': 'user_metadata',
        'expires_at': None,
        'revocable': False,
        'billing_required': False,
    })
    assert provider.entitlement_for(VerifiedIdentity('user-1', 'supabase')) == FREE_ENTITLEMENT


def test_repository_failure_fails_closed_to_free():
    def broken_lookup(subject: str):
        raise RuntimeError('database unavailable')

    provider = RepositoryEntitlementProvider(broken_lookup)
    assert provider.entitlement_for(VerifiedIdentity('user-1', 'supabase')) == FREE_ENTITLEMENT
