from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime
from typing import Any

from nextlaw607.access import (
    Entitlement,
    FOUNDER_ENTITLEMENT,
    FREE_ENTITLEMENT,
    VerifiedIdentity,
)

EntitlementLookup = Callable[[str], Mapping[str, Any] | None]

_ALLOWED_PAID_TIERS = {"premium", "case_pass", "pro", "institutional"}
_ALLOWED_SOURCES = {"purchase", "institutional_grant"}


class RepositoryEntitlementProvider:
    """Resolve paid access from an authoritative server-side repository.

    Repository outages, malformed rows, and unknown values fail closed to Free.
    Founder grants are canonicalized so mutable storage fields cannot make them
    expiring, billable, or normally revocable.
    """

    def __init__(self, lookup: EntitlementLookup) -> None:
        self._lookup = lookup

    def entitlement_for(self, identity: VerifiedIdentity) -> Entitlement:
        try:
            record = self._lookup(identity.subject)
        except Exception:
            return FREE_ENTITLEMENT

        if not isinstance(record, Mapping):
            return FREE_ENTITLEMENT

        source = record.get("source")
        if source == "founder_lifetime_grant":
            return FOUNDER_ENTITLEMENT

        tier = record.get("tier")
        expires_at = record.get("expires_at")
        revocable = record.get("revocable")
        billing_required = record.get("billing_required")

        if tier not in _ALLOWED_PAID_TIERS or source not in _ALLOWED_SOURCES:
            return FREE_ENTITLEMENT
        if not isinstance(revocable, bool) or not isinstance(billing_required, bool):
            return FREE_ENTITLEMENT
        if expires_at is not None:
            if not isinstance(expires_at, str) or not expires_at.strip():
                return FREE_ENTITLEMENT
            try:
                datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            except ValueError:
                return FREE_ENTITLEMENT
            expires_at = expires_at.strip()

        return Entitlement(
            tier=tier,
            source=source,
            expires_at=expires_at,
            revocable=revocable,
            billing_required=billing_required,
        )
