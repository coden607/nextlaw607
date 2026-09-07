from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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


class SupabaseEntitlementLookup:
    """Server-only PostgREST lookup for NextLaw authoritative entitlements."""

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
        if not normalized_key.startswith("sb_secret_"):
            raise ValueError("Supabase secret key is required for entitlement lookup")
        if timeout <= 0:
            raise ValueError("Supabase entitlement timeout must be positive")

        self._project_url = normalized_url
        self._secret_key = normalized_key
        self._timeout = float(timeout)
        self._request_json = request_json or _stdlib_request_json

    def __call__(self, subject: str) -> Mapping[str, Any] | None:
        normalized_subject = subject.strip()
        if not normalized_subject:
            return None

        query = urlencode(
            {
                "user_id": f"eq.{normalized_subject}",
                "select": "tier,source,expires_at,revocable,billing_required",
                "limit": "1",
            }
        )
        url = f"{self._project_url}/rest/v1/entitlements?{query}"

        try:
            status, payload = self._request_json(
                url,
                {
                    "apikey": self._secret_key,
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
