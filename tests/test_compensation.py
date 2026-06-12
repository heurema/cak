"""Compensation/saga slice: prepared, suggested, executed (docs/19)."""

import io
import json
from pathlib import Path
from typing import Any

import pytest

from cak.gateway import Gateway
from cak.specs import GatewayConfig, load_config_file
from cak.trace import TraceRecorder, read_trace

CONFIG_PATH = Path(__file__).resolve().parents[1] / "examples" / "v0_1" / "gateway_config.json"


@pytest.fixture()
def config() -> GatewayConfig:
    return load_config_file(CONFIG_PATH)


def _gateway(config: GatewayConfig, trace_path: Path) -> Gateway:
    return Gateway(
        config=config,
        identity="billing-agent",
        recorder=TraceRecorder(trace_path),
        upstream_in=io.BytesIO(),
        upstream_out=io.BytesIO(),
        client_in=io.BytesIO(),
        client_out=io.BytesIO(),
    )


def _client_call(gateway: Gateway, call_id: int, action: str,
                 arguments: dict[str, Any]) -> None:
    request = {
        "jsonrpc": "2.0", "id": call_id, "method": "tools/call",
        "params": {"name": action, "arguments": arguments},
    }
    gateway.handle_client_message(json.dumps(request).encode(), framed=False)


def _upstream_result(gateway: Gateway, call_id: int, payload: dict[str, Any]) -> None:
    response = {
        "jsonrpc": "2.0", "id": call_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(payload)}],
            "structuredContent": payload,
            "isError": False,
        },
    }
    gateway.handle_upstream_message(json.dumps(response).encode())


CREATE_ARGS = {
    "customer_email": "jane@example.com",
    "amount": 500,
    "due_date": "2026-07-01",
}


def test_compensation_prepared_with_derived_args(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "t.jsonl"
    gateway = _gateway(config, trace_path)
    _client_call(gateway, 1, "crm.create_invoice", CREATE_ARGS)
    _upstream_result(gateway, 1, {"invoice": {"id": "inv_001", "status": "draft"}})

    events = read_trace(trace_path)
    prepared = next(e for e in events if e["type"] == "compensation_prepared")
    assert prepared["call_id"] == 1
    assert prepared["action"] == "crm.void_invoice"
    assert prepared["arguments"] == {"invoice_id": "inv_001"}
    assert all(e["type"] != "compensation_suggested" for e in events)


def test_postcondition_failure_suggests_compensation(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "t.jsonl"
    gateway = _gateway(config, trace_path)
    _client_call(gateway, 1, "crm.create_invoice", CREATE_ARGS)
    # Upstream reports a state that violates the declared effect.
    _upstream_result(gateway, 1, {"invoice": {"id": "inv_001", "status": "failed"}})

    events = read_trace(trace_path)
    suggested = next(e for e in events if e["type"] == "compensation_suggested")
    assert suggested["failed_postconditions"] == ['invoice.status == "draft"']
    assert suggested["compensation"]["arguments"] == {"invoice_id": "inv_001"}


def test_executed_compensation_links_saga_chain(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "t.jsonl"
    gateway = _gateway(config, trace_path)
    _client_call(gateway, 1, "crm.create_invoice", CREATE_ARGS)
    _upstream_result(gateway, 1, {"invoice": {"id": "inv_001", "status": "draft"}})

    # The agent fires the prepared call; it is verified like any action.
    _client_call(gateway, 2, "crm.void_invoice", {"invoice_id": "inv_001"})
    _upstream_result(gateway, 2, {"invoice": {"id": "inv_001", "status": "void"}})

    events = read_trace(trace_path)
    executed = next(e for e in events if e["type"] == "compensation_executed")
    assert executed["call_id"] == 2
    assert executed["compensates_call_id"] == 1
    # The compensation call itself was verified and postcondition-checked.
    void_decision = next(
        e for e in events if e["type"] == "decision" and e["call_id"] == 2
    )
    assert void_decision["decision"]["enforcement"] == "allow"
    void_post = next(
        e for e in events if e["type"] == "postconditions" and e["call_id"] == 2
    )
    assert void_post["checks"]['invoice.status == "void"'] == "true"


def test_unrelated_call_does_not_claim_the_chain(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "t.jsonl"
    gateway = _gateway(config, trace_path)
    _client_call(gateway, 1, "crm.create_invoice", CREATE_ARGS)
    _upstream_result(gateway, 1, {"invoice": {"id": "inv_001", "status": "draft"}})

    # Different invoice id -> different args hash -> no linkage.
    _client_call(gateway, 2, "crm.void_invoice", {"invoice_id": "inv_999"})
    _upstream_result(gateway, 2, {"invoice": {"id": "inv_999", "status": "void"}})

    events = read_trace(trace_path)
    assert all(e["type"] != "compensation_executed" for e in events)


def test_unresolvable_paths_prepare_nothing(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "t.jsonl"
    gateway = _gateway(config, trace_path)
    _client_call(gateway, 1, "crm.create_invoice", CREATE_ARGS)
    # Result lacks invoice.id: the derivation must refuse, not guess.
    _upstream_result(gateway, 1, {"invoice": {"status": "draft"}})

    events = read_trace(trace_path)
    assert all(e["type"] != "compensation_prepared" for e in events)
