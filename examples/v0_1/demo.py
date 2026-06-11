"""End-to-end v0.1 demo (docs/13 success criteria, docs/17 demo consequence).

Runs the CAK gateway in front of the mock CRM server and shows what plain
gateways cannot express:

    amount 500    -> auto-allow as Effect<compensable>, postcondition checked
    amount 20000  -> require_approval (typed denial with queued request id)
                  -> operator grants a scoped single-use token
                  -> identical retry is forwarded, postcondition checked
    amount -5     -> block (precondition named)

Then replays the recorded trace and prints checkpoint fidelity.

Usage:  PYTHONPATH=src python3 examples/v0_1/demo.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import IO, Any

from cak.approvals import ApprovalStore
from cak.replay import replay
from cak.specs import load_config_file

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "examples" / "v0_1" / "gateway_config.json"
MOCK = ROOT / "examples" / "v0_1" / "mock_crm_server.py"


def rpc(stdin: IO[bytes], stdout: IO[bytes], request: dict[str, Any]) -> dict[str, Any]:
    stdin.write(json.dumps(request).encode() + b"\n")
    stdin.flush()
    line = stdout.readline()
    response: dict[str, Any] = json.loads(line)
    return response


def _call_request(call_id: int, amount: float) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0", "id": call_id, "method": "tools/call",
        "params": {
            "name": "crm.create_invoice",
            "arguments": {
                "customer_email": "jane@example.com",
                "amount": amount,
                "due_date": "2026-07-01",
            },
        },
    }


def main() -> int:
    trace_path = Path(tempfile.mkstemp(suffix=".trace.jsonl")[1])
    approvals_path = Path(tempfile.mkdtemp(suffix=".approvals"))
    gateway = subprocess.Popen(
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
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"},
    )
    assert gateway.stdin is not None and gateway.stdout is not None

    rpc(gateway.stdin, gateway.stdout,
        {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}})

    print("--- auto-allow + postcondition (amount=500)")
    response = rpc(gateway.stdin, gateway.stdout, _call_request(1, 500))
    print(json.dumps(response["result"], indent=2, ensure_ascii=False))

    print("--- require approval (amount=20000)")
    response = rpc(gateway.stdin, gateway.stdout, _call_request(2, 20000))
    print(json.dumps(response["result"], indent=2, ensure_ascii=False))
    payload = json.loads(response["result"]["content"][0]["text"])
    request_id = payload["approval_request_id"]

    print(f"--- operator grants request {request_id} (scoped, single-use, 15 min TTL)")
    ApprovalStore(approvals_path).grant(request_id, approver="demo-operator")

    print("--- identical retry after approval (amount=20000)")
    response = rpc(gateway.stdin, gateway.stdout, _call_request(3, 20000))
    print(json.dumps(response["result"], indent=2, ensure_ascii=False))

    print("--- block (amount=-5)")
    response = rpc(gateway.stdin, gateway.stdout, _call_request(4, -5))
    print(json.dumps(response["result"], indent=2, ensure_ascii=False))

    gateway.stdin.close()
    gateway.wait(timeout=5)

    print("--- trace events")
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        print(f"  seq={event['seq']} type={event['type']} call_id={event.get('call_id')}")

    report = replay(load_config_file(CONFIG), trace_path)
    print("--- replay")
    print(
        f"  proposals={report.proposals} decisions_checked={report.decisions_checked} "
        f"postconditions_checked={report.postconditions_checked} ok={report.ok}"
    )
    for divergence in report.divergences:
        print(f"  divergence: {divergence}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
