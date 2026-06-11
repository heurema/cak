"""File-based approval queue and tokens for `require_approval` decisions.

Approval semantics per docs/07: typed, scoped, logged, expiring.

- Scope is exact: identity + action + sha256 of canonical arguments. A token
  approves one specific call, not a session and not an action class.
- Tokens are single-use: consumed on the first matching retry.
- Tokens expire (default 15 minutes).
- The queue is plain JSON files under one directory — local-first,
  inspectable, no daemon. Chat/webhook adapters are a later concern.

Flow:

    agent call -> require_approval -> pending request (typed denial carries
    the request id) -> human grants via `python -m cak.approve` -> agent
    retries the same call -> gateway consumes the token and forwards.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_TTL_SECONDS = 900


class ApprovalError(ValueError):
    """Raised on invalid approval-store operations."""


def args_hash(arguments: dict[str, Any]) -> str:
    canonical = json.dumps(arguments, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ApprovalStore:
    root: Path

    def __post_init__(self) -> None:
        for state in ("pending", "granted", "denied"):
            (self.root / state).mkdir(parents=True, exist_ok=True)

    # -- helpers -----------------------------------------------------------

    def _path(self, state: str, request_id: str) -> Path:
        return self.root / state / f"{request_id}.json"

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return data

    @staticmethod
    def _write(path: Path, record: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    # -- queue -------------------------------------------------------------

    def request(
        self,
        identity: str,
        action: str,
        arguments: dict[str, Any],
        decision: dict[str, Any],
    ) -> str:
        """Queue an approval request; dedupe identical pending scopes."""
        scope_hash = args_hash(arguments)
        for existing in self.list_pending():
            if (
                existing["identity"] == identity
                and existing["action"] == action
                and existing["args_hash"] == scope_hash
            ):
                return str(existing["request_id"])

        request_id = uuid.uuid4().hex[:12]
        self._write(
            self._path("pending", request_id),
            {
                "request_id": request_id,
                "requested_at": time.time(),
                "identity": identity,
                "action": action,
                "arguments": arguments,
                "args_hash": scope_hash,
                "decision": decision,
            },
        )
        return request_id

    def list_pending(self) -> list[dict[str, Any]]:
        return sorted(
            (self._read(path) for path in (self.root / "pending").glob("*.json")),
            key=lambda record: float(record["requested_at"]),
        )

    def grant(
        self,
        request_id: str,
        approver: str,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
    ) -> dict[str, Any]:
        pending = self._path("pending", request_id)
        if not pending.exists():
            raise ApprovalError(f"no pending approval request '{request_id}'")
        record = self._read(pending)
        record.update(
            approved_by=approver,
            approved_at=time.time(),
            expires_at=time.time() + ttl_seconds,
            used=False,
        )
        self._write(self._path("granted", request_id), record)
        pending.unlink()
        return record

    def deny(self, request_id: str, approver: str) -> dict[str, Any]:
        pending = self._path("pending", request_id)
        if not pending.exists():
            raise ApprovalError(f"no pending approval request '{request_id}'")
        record = self._read(pending)
        record.update(denied_by=approver, denied_at=time.time())
        self._write(self._path("denied", request_id), record)
        pending.unlink()
        return record

    def consume(
        self, identity: str, action: str, arguments: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Find a valid token for this exact call; mark it used."""
        scope_hash = args_hash(arguments)
        now = time.time()
        for path in sorted((self.root / "granted").glob("*.json")):
            record = self._read(path)
            if (
                record["identity"] == identity
                and record["action"] == action
                and record["args_hash"] == scope_hash
                and not record.get("used", False)
                and now <= float(record["expires_at"])
            ):
                record["used"] = True
                record["used_at"] = now
                self._write(path, record)
                return record
        return None
