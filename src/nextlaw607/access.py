from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Protocol

EntitlementTier = Literal["free", "premium", "case_pass", "pro", "institutional"]
EntitlementSource = Literal[
    "default_free",
    "purchase",
    "institutional_grant",
    "founder_lifetime_grant",
]


@dataclass(frozen=True, slots=True)
class VerifiedIdentity:
    subject: str
    provider: str


@dataclass(frozen=True, slots=True)
class Entitlement:
    tier: EntitlementTier
    source: EntitlementSource
    expires_at: str | None
    revocable: bool
    billing_required: bool

    def has_premium_access(self, now: datetime | None = None) -> bool:
        if self.tier not in {"premium", "case_pass", "pro", "institutional"}:
            return False
        if self.expires_at is None:
            return True
        try:
            expires = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        except ValueError:
            return False
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)
        return expires > current

    def as_dict(self) -> dict[str, object]:
        return {
            "tier": self.tier,
            "source": self.source,
            "expires_at": self.expires_at,
            "revocable": self.revocable,
            "billing_required": self.billing_required,
        }


FREE_ENTITLEMENT = Entitlement(
    tier="free",
    source="default_free",
    expires_at=None,
    revocable=True,
    billing_required=False,
)

FOUNDER_ENTITLEMENT = Entitlement(
    tier="premium",
    source="founder_lifetime_grant",
    expires_at=None,
    revocable=False,
    billing_required=False,
)


class IdentityProvider(Protocol):
    def verify_bearer_token(self, token: str) -> VerifiedIdentity | None: ...


class EntitlementProvider(Protocol):
    def entitlement_for(self, identity: VerifiedIdentity) -> Entitlement: ...


class RejectingIdentityProvider:
    """Safe default until a real identity provider adapter is configured."""

    def verify_bearer_token(self, token: str) -> VerifiedIdentity | None:
        return None


class FreeEntitlementProvider:
    """Safe default: authenticated identities receive no paid grant implicitly."""

    def entitlement_for(self, identity: VerifiedIdentity) -> Entitlement:
        return FREE_ENTITLEMENT


class IdentityVerificationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class AccessContext:
    identity_kind: Literal["guest", "authenticated"]
    subject: str | None
    provider: str
    entitlement: Entitlement

    @property
    def premium_access(self) -> bool:
        return self.entitlement.has_premium_access()

    def as_dict(self) -> dict[str, object]:
        return {
            "identity": {
                "kind": self.identity_kind,
                "subject": self.subject,
                "provider": self.provider,
            },
            "entitlement": self.entitlement.as_dict(),
            "premium_access": self.premium_access,
        }


def resolve_access(
    authorization: str | None,
    identity_provider: IdentityProvider,
    entitlement_provider: EntitlementProvider,
) -> AccessContext:
    if authorization is None:
        return AccessContext(
            identity_kind="guest",
            subject=None,
            provider="local",
            entitlement=FREE_ENTITLEMENT,
        )

    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token.strip():
        raise IdentityVerificationError("identity verification failed")

    verified = identity_provider.verify_bearer_token(token.strip())
    if verified is None or not verified.subject.strip() or not verified.provider.strip():
        raise IdentityVerificationError("identity verification failed")

    entitlement = entitlement_provider.entitlement_for(verified)
    return AccessContext(
        identity_kind="authenticated",
        subject=verified.subject,
        provider=verified.provider,
        entitlement=entitlement,
    )
