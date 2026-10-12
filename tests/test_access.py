from datetime import datetime, timezone

import pytest

from nextlaw607.access import (
    AccessContext,
    Entitlement,
    FOUNDER_ENTITLEMENT,
    FREE_ENTITLEMENT,
    PremiumAccessRequired,
    ensure_premium,
)


def test_server_premium_guard_rejects_guest_free_access():
    access = AccessContext(
        identity_kind='guest',
        subject=None,
        provider='local',
        entitlement=FREE_ENTITLEMENT,
    )
    with pytest.raises(PremiumAccessRequired, match='premium access required'):
        ensure_premium(access)


def test_server_premium_guard_accepts_founder_lifetime_grant():
    access = AccessContext(
        identity_kind='authenticated',
        subject='founder-1',
        provider='verified-provider',
        entitlement=FOUNDER_ENTITLEMENT,
    )
    assert ensure_premium(access) is access


def test_server_premium_guard_rejects_expired_paid_access():
    access = AccessContext(
        identity_kind='authenticated',
        subject='user-1',
        provider='verified-provider',
        entitlement=Entitlement(
            tier='premium',
            source='purchase',
            expires_at='2026-01-01T00:00:00+00:00',
            revocable=True,
            billing_required=True,
        ),
    )
    with pytest.raises(PremiumAccessRequired, match='premium access required'):
        ensure_premium(access, now=datetime(2026, 9, 7, tzinfo=timezone.utc))
