from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_SECRET_KEY_RE = re.compile(r"\b(?:sk|sb_secret)_[A-Za-z0-9._-]{8,}\b|\bsk-[A-Za-z0-9._-]{8,}\b")


def _clean_identifier(value: str, name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} is required")
    if normalized == "*":
        raise ValueError(f"{name} wildcard is not allowed")
    return normalized


def redact_memory_text(content: str) -> str:
    if not isinstance(content, str) or not content.strip():
        raise ValueError("memory content is required")
    redacted = _BEARER_RE.sub("Bearer [REDACTED]", content)
    return _SECRET_KEY_RE.sub("[REDACTED]", redacted).strip()


@dataclass(frozen=True)
class MemoryScope:
    user_id: str
    case_id: str
    agent_id: str
    session_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "user_id", _clean_identifier(self.user_id, "user_id"))
        object.__setattr__(self, "case_id", _clean_identifier(self.case_id, "case_id"))
        object.__setattr__(self, "agent_id", _clean_identifier(self.agent_id, "agent_id"))
        object.__setattr__(self, "session_id", _clean_identifier(self.session_id, "session_id"))


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    content: str
    scope: MemoryScope
    authority_eligible: bool = False


def _scope_fingerprint(scope: MemoryScope) -> str:
    """Return a deterministic opaque attestation for the complete NextLaw memory scope."""
    canonical = json.dumps(
        [scope.user_id, scope.case_id, scope.agent_id, scope.session_id],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


class MemoryVault:
    """Deterministic in-process memory boundary used by tests and local fallback.

    The vault intentionally models the privacy and legal-trust contract without
    depending on any external memory provider. Production adapters must preserve
    these same semantics.
    """

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def remember(self, content: str, *, scope: MemoryScope, consent: bool) -> MemoryRecord:
        if consent is not True:
            raise PermissionError("explicit memory consent is required")
        record = MemoryRecord(
            memory_id=uuid4().hex,
            content=redact_memory_text(content),
            scope=scope,
            authority_eligible=False,
        )
        self._records[record.memory_id] = record
        return record

    def export(self, scope: MemoryScope) -> tuple[MemoryRecord, ...]:
        return tuple(record for record in self._records.values() if record.scope == scope)

    def delete(self, scope: MemoryScope) -> int:
        ids = [record.memory_id for record in self.export(scope)]
        for memory_id in ids:
            self._records.pop(memory_id, None)
        return len(ids)


class Mem0MemoryAdapter:
    """Mem0 adapter that preserves NextLaw's exact-scope privacy boundary.

    `backend` is intentionally duck-typed so the boundary can be verified without
    network calls. It is compatible with Mem0 clients exposing add/get_all/delete.
    Bulk wildcard deletion is deliberately not used; exact records are enumerated
    and deleted by memory id.

    Provider-side filtering is treated as defense-in-depth rather than authority:
    every accepted provider record must carry the opaque NextLaw scope fingerprint
    written at creation time. A missing or mismatched attestation fails closed.
    """

    def __init__(self, backend: Any) -> None:
        if backend is None:
            raise ValueError("Mem0 backend is required")
        self._backend = backend

    @staticmethod
    def _filters(scope: MemoryScope) -> dict[str, list[dict[str, str]]]:
        return {
            "AND": [
                {"user_id": scope.user_id},
                {"agent_id": scope.agent_id},
                {"run_id": scope.session_id},
                {"metadata.case_id": scope.case_id},
            ]
        }

    def remember(self, content: str, *, scope: MemoryScope, consent: bool) -> MemoryRecord:
        if consent is not True:
            raise PermissionError("explicit memory consent is required")
        sanitized = redact_memory_text(content)
        result = self._backend.add(
            [{"role": "user", "content": sanitized}],
            user_id=scope.user_id,
            agent_id=scope.agent_id,
            run_id=scope.session_id,
            metadata={
                "case_id": scope.case_id,
                "authority_eligible": False,
                "nextlaw_scope_version": 1,
                "nextlaw_scope_fingerprint": _scope_fingerprint(scope),
            },
        )
        memory_id = self._extract_created_id(result) or uuid4().hex
        return MemoryRecord(memory_id, sanitized, scope, False)

    def export(self, scope: MemoryScope) -> tuple[MemoryRecord, ...]:
        payload = self._backend.get_all(filters=self._filters(scope))
        results = payload.get("results", []) if isinstance(payload, dict) else []
        records: list[MemoryRecord] = []
        expected_fingerprint = _scope_fingerprint(scope)
        for item in results:
            if not isinstance(item, dict):
                continue
            metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
            if metadata.get("case_id") != scope.case_id:
                continue
            if metadata.get("nextlaw_scope_version") != 1:
                continue
            if metadata.get("nextlaw_scope_fingerprint") != expected_fingerprint:
                continue
            if metadata.get("authority_eligible") is not False:
                continue
            memory_id = item.get("id")
            content = item.get("memory", item.get("text", ""))
            if not isinstance(memory_id, str) or not memory_id.strip():
                continue
            if not isinstance(content, str) or not content.strip():
                continue
            records.append(
                MemoryRecord(
                    memory_id=memory_id.strip(),
                    content=redact_memory_text(content),
                    scope=scope,
                    authority_eligible=False,
                )
            )
        return tuple(records)

    def delete(self, scope: MemoryScope) -> int:
        records = self.export(scope)
        for record in records:
            self._backend.delete(record.memory_id)
        return len(records)

    @staticmethod
    def _extract_created_id(result: Any) -> str | None:
        if not isinstance(result, dict):
            return None
        results = result.get("results")
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    value = item["id"].strip()
                    if value:
                        return value
        return None


def memory_can_verify_authority(record: MemoryRecord) -> bool:
    """Memory is context only; it can never satisfy legal-authority verification."""
    return False
