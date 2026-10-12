from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

RequestJson = Callable[[str, dict[str, str], float], tuple[int, Any]]

_SELECT_FIELDS = "tier%2Csource%2Cexpires_at%2Crevocable%2Cbilling_required"


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


class SupabaseEntitlementRepository:
    """Server-only authoritative entitlement lookup.

    The repository accepts no client-supplied tier or billing metadata. Any
    transport, status, shape, or cardinality anomaly fails closed by returning
    no grant; RepositoryEntitlementProvider then resolves the user to Free.
    """

    def __init__(
        self,
        project_url: str,
        secret_key: str,
        *,
        timeout: float = 5.0,
        request_json: RequestJson | None = None,
    ) -> None:
        normalized_url = project_url.strip().rstrip("/")
        normalized_key = secret_key.strip()
        if not normalized_url.startswith("https://"):
            raise ValueError("Supabase project URL must use https")
        if not normalized_key:
            raise ValueError("Supabase server secret key is required")
        if normalized_key.startswith("sb_publishable_"):
            raise ValueError("Supabase server secret key must not be a publishable key")
        if timeout <= 0:
            raise ValueError("Supabase entitlement timeout must be positive")

        self._project_url = normalized_url
        self._secret_key = normalized_key
        self._timeout = float(timeout)
        self._request_json = request_json or _stdlib_request_json

    def lookup(self, subject: str) -> Mapping[str, Any] | None:
        normalized_subject = subject.strip()
        if not normalized_subject:
            return None

        encoded_subject = quote(normalized_subject, safe="")
        url = (
            f"{self._project_url}/rest/v1/entitlements"
            f"?user_id=eq.{encoded_subject}&select={_SELECT_FIELDS}&limit=1"
        )
        try:
            status, payload = self._request_json(
                url,
                {
                    "apikey": self._secret_key,
                    "Authorization": f"Bearer {self._secret_key}",
                    "Accept": "application/json",
                },
                self._timeout,
            )
        except Exception:
            return None

        if status != 200 or not isinstance(payload, list) or len(payload) != 1:
            return None
        row = payload[0]
        if not isinstance(row, Mapping):
            return None
        return row
