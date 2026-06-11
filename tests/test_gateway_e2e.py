"""End-to-end: real gateway subprocess in front of the mock CRM server."""

import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import IO, Any

import pytest

from cak.approvals import ApprovalStore
from cak.mcp_stdio import encode_message, read_message
from cak.replay import replay
from cak.specs import load_config_file
from cak.trace import read_trace

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "examples" / "v0_1" / "gateway_config.json"
MOCK = ROOT / "examples" / "v0_1" / "mock_crm_server.py"


def _rpc(stdin: IO[bytes], stdout: IO[bytes], request: dict[str, Any]) -> dict[str, Any]:
    stdin.write(json.dumps(request).encode() + b"\n")
    stdin.flush()
    response: dict[str, Any] = json.loads(stdout.readline())
    return response


def _call(stdin: IO[bytes], stdout: IO[bytes], call_id: int, amount: float) -> dict[str, Any]:
    return _rpc(
        stdin, stdout,
        {
            "jsonrpc": "2.0", "id": call_id, "method": "tools/call",
            "params": {
                "name": "crm.create_invoice",
                "arguments": {
                    "customer_email": "jane@example.com",
                    "amount": amount,
                    "due_date": "2026-07-01",
                },
            },
        },
    )


def _framed_rpc(
    stdin: IO[bytes], stdout: IO[bytes], request: dict[str, Any]
) -> dict[str, Any]:
    stdin.write(encode_message(request, framed=True))
    stdin.flush()
    response = read_message(stdout)
    assert response is not None
    assert response.framed
    parsed: dict[str, Any] = json.loads(response.payload)
    return parsed


def _framed_call(
    stdin: IO[bytes], stdout: IO[bytes], call_id: int, amount: float
) -> dict[str, Any]:
    return _framed_rpc(
        stdin,
        stdout,
        {
            "jsonrpc": "2.0",
            "id": call_id,
            "method": "tools/call",
            "params": {
                "name": "crm.create_invoice",
                "arguments": {
                    "customer_email": "jane@example.com",
                    "amount": amount,
                    "due_date": "2026-07-01",
                },
            },
        },
    )


@pytest.fixture()
def gateway(tmp_path: Path) -> Iterator[tuple[subprocess.Popen[bytes], Path, Path]]:
    trace_path = tmp_path / "session.jsonl"
    approvals_path = tmp_path / "approvals"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    process = subprocess.Popen(
        [
            sys.executable, "-m", "cak.gateway",
            "--config", str(CONFIG),
            "--identity", "billing-agent",
            "--trace", str(trace_path),
            "--approvals", str(approvals_path),
            "--", sys.executable, str(MOCK),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=env,
    )
    try:
        yield process, trace_path, approvals_path
    finally:
        if process.stdin is not None:
            process.stdin.close()
        process.terminate()
        process.wait(timeout=5)


def test_end_to_end_allow_approve_block(
    gateway: tuple[subprocess.Popen[bytes], Path, Path],
) -> None:
    process, trace_path, approvals_path = gateway
    assert process.stdin is not None and process.stdout is not None

    init = _rpc(process.stdin, process.stdout,
                {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}})
    assert init["result"]["serverInfo"]["name"] == "mock-crm"

    allowed = _call(process.stdin, process.stdout, 1, 500)
    invoice = allowed["result"]["structuredContent"]["invoice"]
    assert invoice["status"] == "draft"

    approval = _call(process.stdin, process.stdout, 2, 20000)
    payload = json.loads(approval["result"]["content"][0]["text"])
    denial = payload["cak_denial"]
    assert approval["result"]["isError"] is True
    assert denial["enforcement"] == "require_approval"
    assert denial["fired_policies"] == ["policy.high_amount_requires_approval"]
    assert denial["effect_id"] == "effect.crm.create_invoice"
    assert payload["retry_after_approval"] is True

    # Human grants the queued request; the identical retry is forwarded.
    store = ApprovalStore(approvals_path)
    store.grant(payload["approval_request_id"], approver="test-operator")
    retried = _call(process.stdin, process.stdout, 3, 20000)
    assert retried["result"]["structuredContent"]["invoice"]["status"] == "draft"

    # The token was single-use: the same call needs approval again.
    repeated = _call(process.stdin, process.stdout, 4, 20000)
    assert json.loads(repeated["result"]["content"][0]["text"])[
        "cak_denial"]["enforcement"] == "require_approval"

    blocked = _call(process.stdin, process.stdout, 5, -5)
    denial = json.loads(blocked["result"]["content"][0]["text"])["cak_denial"]
    assert denial["enforcement"] == "block"

    if process.stdin is not None:
        process.stdin.close()
    process.wait(timeout=5)

    events = read_trace(trace_path)
    types = [event["type"] for event in events]
    assert types.count("proposal") == 5
    assert types.count("decision") == 5
    assert types.count("approval_requested") == 2
    assert types.count("approval_consumed") == 1
    assert types.count("outcome") == 2  # allowed call + approved retry
    assert types.count("postconditions") == 2

    consumed = next(e for e in events if e["type"] == "approval_consumed")
    assert consumed["approved_by"] == "test-operator"

    postconditions = next(e for e in events if e["type"] == "postconditions")
    assert postconditions["checks"]['invoice.status == "draft"'] == "true"
    assert postconditions["checks"]["invoice.id.present"] == "true"

    report = replay(load_config_file(CONFIG), trace_path)
    assert report.ok
    assert report.proposals == 5
    assert report.decisions_checked == 5
    assert report.postconditions_checked == 2


def test_gateway_accepts_mcp_stdio_framing(
    gateway: tuple[subprocess.Popen[bytes], Path, Path],
) -> None:
    process, trace_path, approvals_path = gateway
    assert process.stdin is not None and process.stdout is not None

    init = _framed_rpc(
        process.stdin,
        process.stdout,
        {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}},
    )
    assert init["result"]["serverInfo"]["name"] == "mock-crm"

    resources = _framed_rpc(
        process.stdin,
        process.stdout,
        {"jsonrpc": "2.0", "id": 1, "method": "resources/list", "params": {}},
    )
    assert resources["result"]["resources"] == []

    tools = _framed_rpc(
        process.stdin,
        process.stdout,
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    )
    create_invoice = next(
        tool for tool in tools["result"]["tools"] if tool["name"] == "crm.create_invoice"
    )
    assert create_invoice["inputSchema"]["required"] == [
        "customer_email", "amount", "due_date"
    ]

    allowed = _framed_call(process.stdin, process.stdout, 3, 500)
    assert allowed["result"]["structuredContent"]["invoice"]["status"] == "draft"

    approval = _framed_call(process.stdin, process.stdout, 4, 20000)
    payload = json.loads(approval["result"]["content"][0]["text"])
    assert payload["cak_denial"]["enforcement"] == "require_approval"
    ApprovalStore(approvals_path).grant(
        payload["approval_request_id"], approver="test-operator"
    )

    retried = _framed_call(process.stdin, process.stdout, 5, 20000)
    assert retried["result"]["structuredContent"]["invoice"]["status"] == "draft"

    repeated = _framed_call(process.stdin, process.stdout, 6, 20000)
    assert json.loads(repeated["result"]["content"][0]["text"])[
        "cak_denial"]["enforcement"] == "require_approval"

    blocked = _framed_call(process.stdin, process.stdout, 7, -5)
    assert json.loads(blocked["result"]["content"][0]["text"])[
        "cak_denial"]["enforcement"] == "block"

    process.stdin.close()
    process.wait(timeout=5)

    report = replay(load_config_file(CONFIG), trace_path)
    assert report.ok
    assert report.proposals == 5
    assert report.decisions_checked == 5
    assert report.postconditions_checked == 2
