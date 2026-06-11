import time
from pathlib import Path

import pytest

from cak.approvals import ApprovalError, ApprovalStore

ARGS = {"customer_email": "jane@example.com", "amount": 20000, "due_date": "2026-07-01"}
DECISION = {"enforcement": "require_approval"}


@pytest.fixture()
def store(tmp_path: Path) -> ApprovalStore:
    return ApprovalStore(tmp_path / "approvals")


def test_request_grant_consume(store: ApprovalStore) -> None:
    request_id = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    assert [r["request_id"] for r in store.list_pending()] == [request_id]

    record = store.grant(request_id, approver="vi", ttl_seconds=60)
    assert record["approved_by"] == "vi"
    assert not store.list_pending()

    token = store.consume("billing-agent", "crm.create_invoice", ARGS)
    assert token is not None and token["request_id"] == request_id


def test_token_is_single_use(store: ApprovalStore) -> None:
    request_id = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    store.grant(request_id, approver="vi")
    assert store.consume("billing-agent", "crm.create_invoice", ARGS) is not None
    assert store.consume("billing-agent", "crm.create_invoice", ARGS) is None


def test_token_scope_is_exact(store: ApprovalStore) -> None:
    request_id = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    store.grant(request_id, approver="vi")
    different_args = {**ARGS, "amount": 20001}
    assert store.consume("billing-agent", "crm.create_invoice", different_args) is None
    assert store.consume("other-agent", "crm.create_invoice", ARGS) is None
    assert store.consume("billing-agent", "crm.send_invoice", ARGS) is None


def test_token_expires(store: ApprovalStore) -> None:
    request_id = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    record = store.grant(request_id, approver="vi", ttl_seconds=60)
    # Force expiry by rewriting the token with a past deadline.
    record["expires_at"] = time.time() - 1
    store._write(store._path("granted", request_id), record)
    assert store.consume("billing-agent", "crm.create_invoice", ARGS) is None


def test_pending_requests_dedupe_by_scope(store: ApprovalStore) -> None:
    first = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    second = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    assert first == second
    assert len(store.list_pending()) == 1


def test_deny_removes_pending(store: ApprovalStore) -> None:
    request_id = store.request("billing-agent", "crm.create_invoice", ARGS, DECISION)
    store.deny(request_id, approver="vi")
    assert not store.list_pending()
    assert store.consume("billing-agent", "crm.create_invoice", ARGS) is None
    with pytest.raises(ApprovalError):
        store.grant(request_id, approver="vi")
