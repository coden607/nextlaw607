from __future__ import annotations

from collections.abc import Mapping

from nextlaw607.access import (
    EntitlementProvider,
    FreeEntitlementProvider,
    IdentityProvider,
    RejectingIdentityProvider,
)
from nextlaw607.entitlement_store import RepositoryEntitlementProvider
from nextlaw607.supabase_entitlements import SupabaseEntitlementRepository
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


def entitlement_provider_from_environment(environment: Mapping[str, str]) -> EntitlementProvider:
    project_url = environment.get("SUPABASE_URL", "").strip()
    secret_key = environment.get("SUPABASE_SECRET_KEY", "").strip()

    if not project_url and not secret_key:
        return FreeEntitlementProvider()
    if not project_url or not secret_key:
        raise AccessConfigurationError(
            "SUPABASE_URL and SUPABASE_SECRET_KEY must be configured together"
        )
    if secret_key.startswith("sb_publishable_"):
        raise AccessConfigurationError(
            "SUPABASE_SECRET_KEY must be a server-side secret key, not a publishable key"
        )

    try:
        repository = SupabaseEntitlementRepository(
            project_url=project_url,
            secret_key=secret_key,
        )
    except ValueError as exc:
        raise AccessConfigurationError(str(exc)) from exc
    return RepositoryEntitlementProvider(repository.lookup)
