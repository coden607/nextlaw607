from nextlaw607.supabase_entitlement_lookup import SupabaseEntitlementLookup


def test_secret_entitlement_lookup_queries_exact_verified_subject():
    seen = {}

    def fake_request(url: str, headers: dict[str, str], timeout: float):
        seen.update(url=url, headers=headers, timeout=timeout)
        return 200, [{
            'tier': 'premium',
            'source': 'purchase',
            'expires_at': None,
            'revocable': True,
            'billing_required': True,
        }]

    lookup = SupabaseEntitlementLookup(
        project_url='https://example.supabase.co',
        secret_key='sb_secret_backend_only',
        request_json=fake_request,
    )

    record = lookup('user-123')

    assert record is not None
    assert record['tier'] == 'premium'
    assert seen['url'].startswith('https://example.supabase.co/rest/v1/entitlements?')
    assert 'user_id=eq.user-123' in seen['url']
    assert 'select=tier%2Csource%2Cexpires_at%2Crevocable%2Cbilling_required' in seen['url']
    assert 'limit=1' in seen['url']
    assert seen['headers']['apikey'] == 'sb_secret_backend_only'
    assert 'Authorization' not in seen['headers']
    assert seen['headers']['Accept'] == 'application/json'


def test_entitlement_lookup_rejects_publishable_key_configuration():
    try:
        SupabaseEntitlementLookup(
            project_url='https://example.supabase.co',
            secret_key='sb_publishable_not_allowed',
        )
    except ValueError as exc:
        assert 'secret key' in str(exc).lower()
    else:
        raise AssertionError('publishable key must not configure server entitlement lookup')


def test_entitlement_lookup_rejects_non_https_project_url():
    try:
        SupabaseEntitlementLookup(
            project_url='http://example.supabase.co',
            secret_key='sb_secret_backend_only',
        )
    except ValueError as exc:
        assert 'https' in str(exc).lower()
    else:
        raise AssertionError('non-https project URL must fail closed')


def test_entitlement_lookup_returns_none_on_non_200_response():
    lookup = SupabaseEntitlementLookup(
        project_url='https://example.supabase.co',
        secret_key='sb_secret_backend_only',
        request_json=lambda url, headers, timeout: (403, {'message': 'forbidden'}),
    )
    assert lookup('user-123') is None


def test_entitlement_lookup_returns_none_on_ambiguous_or_malformed_rows():
    ambiguous = SupabaseEntitlementLookup(
        project_url='https://example.supabase.co',
        secret_key='sb_secret_backend_only',
        request_json=lambda url, headers, timeout: (200, [{'tier': 'premium'}, {'tier': 'pro'}]),
    )
    malformed = SupabaseEntitlementLookup(
        project_url='https://example.supabase.co',
        secret_key='sb_secret_backend_only',
        request_json=lambda url, headers, timeout: (200, {'tier': 'premium'}),
    )
    assert ambiguous('user-123') is None
    assert malformed('user-123') is None


def test_entitlement_lookup_transport_failure_returns_none():
    def broken_request(url: str, headers: dict[str, str], timeout: float):
        raise TimeoutError('network unavailable')

    lookup = SupabaseEntitlementLookup(
        project_url='https://example.supabase.co',
        secret_key='sb_secret_backend_only',
        request_json=broken_request,
    )
    assert lookup('user-123') is None
