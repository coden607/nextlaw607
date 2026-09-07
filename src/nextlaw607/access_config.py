from __future__ import annotations

from collections.abc import Mapping

from nextlaw607.access import IdentityProvider, RejectingIdentityProvider
from nextlaw607.supabase_identity import SupabaseIdentityProvider


class AccessConfigurationError(ValueError):
    pass


def identity_provider_from_environment(environment: Mapping[str, str]) -> IdentityProvider:
    project_url = environment.get("SUPABASE_URL", "").strip()
    publishable_key = environment.get("SUPABASE_PUBLISHABLE_KEY", "").strip()

    if not project_url and not publishable_key:
        return RejectingIdentityProvider()
    if not project_url or not publishable_key:
        raise AccessConfigurationError(
            "SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY must be configured together"
        )

    try:
        return SupabaseIdentityProvider(
            project_url=project_url,
            publishable_key=publishable_key,
        )
    except ValueError as exc:
        raise AccessConfigurationError(str(exc)) from exc
