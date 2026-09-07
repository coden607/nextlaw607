from nextlaw607.supabase_entitlements import SupabaseEntitlementRepository


def test_lookup_queries_entitlements_by_exact_subject_and_uses_server_secret():
    calls = []

    def request_json(url, headers, timeout):
        calls.append((url, headers, timeout))
        return 200, [{
            "tier": "pro",
            "source": "purchase",
            "expires_at": None,
            "revocable": True,
            "billing_required": True,
        }]

    repo = SupabaseEntitlementRepository(
        project_url="https://example.supabase.co",
        secret_key="sb_secret_backend_only",
        request_json=request_json,
    )

    record = repo.lookup("user-123")

    assert record == {
        "tier": "pro",
        "source": "purchase",
        "expires_at": None,
        "revocable": True,
        "billing_required": True,
    }
    assert len(calls) == 1
    url, headers, timeout = calls[0]
    assert url == (
        "https://example.supabase.co/rest/v1/entitlements"
        "?user_id=eq.user-123&select=tier%2Csource%2Cexpires_at%2Crevocable%2Cbilling_required&limit=1"
    )
    assert headers["apikey"] == "sb_secret_backend_only"
    assert headers["Authorization"] == "Bearer sb_secret_backend_only"
    assert timeout == 5.0


def test_lookup_url_encodes_subject_instead_of_allowing_filter_injection():
    seen = []

    def request_json(url, headers, timeout):
        seen.append(url)
        return 200, []

    repo = SupabaseEntitlementRepository(
        project_url="https://example.supabase.co",
        secret_key="sb_secret_backend_only",
        request_json=request_json,
    )

    assert repo.lookup("user&or=(tier.eq.pro)") is None
    assert "user%26or%3D%28tier.eq.pro%29" in seen[0]


def test_lookup_fails_closed_on_transport_or_malformed_response():
    responses = [
        (500, {"message": "down"}),
        (200, {"tier": "pro"}),
        (200, []),
        (200, ["not-a-row"]),
        (200, [{"tier": "pro"}, {"tier": "premium"}]),
    ]

    for response in responses:
        repo = SupabaseEntitlementRepository(
            project_url="https://example.supabase.co",
            secret_key="sb_secret_backend_only",
            request_json=lambda url, headers, timeout, response=response: response,
        )
        assert repo.lookup("user-123") is None


def test_repository_requires_https_and_rejects_publishable_key():
    try:
        SupabaseEntitlementRepository(
            project_url="http://example.supabase.co",
            secret_key="sb_secret_backend_only",
        )
        raise AssertionError("http project URL must be rejected")
    except ValueError as exc:
        assert "https" in str(exc)

    try:
        SupabaseEntitlementRepository(
            project_url="https://example.supabase.co",
            secret_key="sb_publishable_not_allowed",
        )
        raise AssertionError("publishable key must be rejected")
    except ValueError as exc:
        assert "secret" in str(exc).lower()
