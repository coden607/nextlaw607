from nextlaw607.supabase_identity import SupabaseIdentityProvider


def test_supabase_identity_verifies_user_through_auth_server():
    seen = {}

    def fake_request(url: str, headers: dict[str, str], timeout: float):
        seen.update(url=url, headers=headers, timeout=timeout)
        return 200, {
            'id': 'user-123',
            'email': 'person@example.com',
            'user_metadata': {'tier': 'premium'},
        }

    provider = SupabaseIdentityProvider(
        project_url='https://example.supabase.co',
        publishable_key='sb_publishable_test',
        request_json=fake_request,
    )

    identity = provider.verify_bearer_token('user-jwt')

    assert identity is not None
    assert identity.subject == 'user-123'
    assert identity.provider == 'supabase'
    assert seen['url'] == 'https://example.supabase.co/auth/v1/user'
    assert seen['headers']['apikey'] == 'sb_publishable_test'
    assert seen['headers']['Authorization'] == 'Bearer user-jwt'
    assert seen['headers']['Accept'] == 'application/json'


def test_supabase_identity_rejects_auth_server_401():
    provider = SupabaseIdentityProvider(
        project_url='https://example.supabase.co',
        publishable_key='sb_publishable_test',
        request_json=lambda url, headers, timeout: (401, {'message': 'invalid token'}),
    )
    assert provider.verify_bearer_token('bad-jwt') is None


def test_supabase_identity_rejects_success_without_user_id():
    provider = SupabaseIdentityProvider(
        project_url='https://example.supabase.co',
        publishable_key='sb_publishable_test',
        request_json=lambda url, headers, timeout: (200, {'user_metadata': {'tier': 'premium'}}),
    )
    assert provider.verify_bearer_token('jwt-without-subject') is None


def test_supabase_identity_rejects_secret_key_configuration():
    try:
        SupabaseIdentityProvider(
            project_url='https://example.supabase.co',
            publishable_key='sb_secret_do_not_use_here',
        )
    except ValueError as exc:
        assert 'publishable key' in str(exc).lower()
    else:
        raise AssertionError('secret key configuration must fail closed')
