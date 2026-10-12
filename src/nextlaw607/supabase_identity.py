from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from nextlaw607.access import VerifiedIdentity

RequestJson = Callable[[str, dict[str, str], float], tuple[int, Any]]


def _stdlib_request_json(
    url: str,
    headers: dict[str, str],
    timeout: float,
) -> tuple[int, Any]:
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            status = int(getattr(response, "status", response.getcode()))
            raw = response.read()
    except HTTPError as exc:
        status = int(exc.code)
        raw = exc.read()
    except (URLError, TimeoutError, OSError):
        return 0, None

    if not raw:
        return status, None
    try:
        return status, json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return status, None


class SupabaseIdentityProvider:
    """Optional Supabase Auth adapter using the Auth server as verifier.

    Entitlements deliberately remain outside this adapter. In particular,
    user-editable user_metadata is never consulted for authorization.
    """

    def __init__(
        self,
        project_url: str,
        publishable_key: str,
        *,
        timeout: float = 5.0,
        request_json: RequestJson | None = None,
    ) -> None:
        normalized_url = project_url.strip().rstrip("/")
        normalized_key = publishable_key.strip()
        if not normalized_url.startswith("https://"):
            raise ValueError("Supabase project URL must use https")
        if not normalized_key:
            raise ValueError("Supabase publishable key is required")
        if normalized_key.startswith("sb_secret_"):
            raise ValueError("Supabase publishable key must not be a secret key")
        if timeout <= 0:
            raise ValueError("Supabase identity timeout must be positive")

        self._project_url = normalized_url
        self._publishable_key = normalized_key
        self._timeout = float(timeout)
        self._request_json = request_json or _stdlib_request_json

    def verify_bearer_token(self, token: str) -> VerifiedIdentity | None:
        normalized_token = token.strip()
        if not normalized_token:
            return None

        try:
            status, payload = self._request_json(
                f"{self._project_url}/auth/v1/user",
                {
                    "apikey": self._publishable_key,
                    "Authorization": f"Bearer {normalized_token}",
                    "Accept": "application/json",
                },
                self._timeout,
            )
        except Exception:
            # Authentication must fail closed if the verifier transport fails.
            return None

        if status != 200 or not isinstance(payload, Mapping):
            return None
        subject = payload.get("id")
        if not isinstance(subject, str) or not subject.strip():
            return None

        return VerifiedIdentity(subject=subject.strip(), provider="supabase")
