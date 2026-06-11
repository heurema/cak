"""End-to-end: real gateway subprocess in front of the mock CRM server."""

import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import IO, Any

import pytest

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


@pytest.fixture()
def gateway(tmp_path: Path) -> Iterator[tuple[subprocess.Popen[bytes], Path]]:
    trace_path = tmp_path / "session.jsonl"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    process = subprocess.Popen(
        [
            sys.executable, "-m", "cak.gateway",
            "--config", str(CONFIG),
            "--identity", "billing-agent",
            "--trace", str(trace_path),
            "--", sys.executable, str(MOCK),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=env,
    )
    try:
        yield process, trace_path
    finally:
        if process.stdin is not None:
            process.stdin.close()
        process.terminate()
        process.wait(timeout=5)


def test_end_to_end_allow_approve_block(
    gateway: tuple[subprocess.Popen[bytes], Path],
) -> None:
    process, trace_path = gateway
    assert process.stdin is not None and process.stdout is not None

    init = _rpc(process.stdin, process.stdout,
                {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}})
    assert init["result"]["serverInfo"]["name"] == "mock-crm"

    allowed = _call(process.stdin, process.stdout, 1, 500)
    invoice = allowed["result"]["structuredContent"]["invoice"]
    assert invoice["status"] == "draft"

    approval = _call(process.stdin, process.stdout, 2, 20000)
    denial = json.loads(approval["result"]["content"][0]["text"])["cak_denial"]
    assert approval["result"]["isError"] is True
    assert denial["enforcement"] == "require_approval"
    assert denial["fired_policies"] == ["policy.high_amount_requires_approval"]
    assert denial["effect_id"] == "effect.crm.create_invoice"

    blocked = _call(process.stdin, process.stdout, 3, -5)
    denial = json.loads(blocked["result"]["content"][0]["text"])["cak_denial"]
    assert denial["enforcement"] == "block"

    if process.stdin is not None:
        process.stdin.close()
    process.wait(timeout=5)

    events = read_trace(trace_path)
    types = [event["type"] for event in events]
    assert types.count("proposal") == 3
    assert types.count("decision") == 3
    assert types.count("outcome") == 1  # only the allowed call reached upstream
    assert types.count("postconditions") == 1

    postconditions = next(e for e in events if e["type"] == "postconditions")
    assert postconditions["checks"]['invoice.status == "draft"'] == "true"
    assert postconditions["checks"]["invoice.id.present"] == "true"

    report = replay(load_config_file(CONFIG), trace_path)
    assert report.ok
    assert report.proposals == 3
    assert report.decisions_checked == 3
    assert report.postconditions_checked == 1
