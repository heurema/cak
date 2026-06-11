"""Mock CRM MCP server (stdio, newline-delimited JSON-RPC) for the v0.1 demo.

Implements just enough of MCP: initialize, tools/list, tools/call for
crm.create_invoice and crm.send_invoice. State is in-memory.
"""

from __future__ import annotations

import json
import sys
from typing import Any

_INVOICES: dict[str, dict[str, Any]] = {}


def _tool_result(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload)}],
        "structuredContent": payload,
        "isError": False,
    }


def _handle_call(params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments") or {}
    if name == "crm.create_invoice":
        invoice_id = f"inv_{len(_INVOICES) + 1:03d}"
        invoice = {
            "id": invoice_id,
            "status": "draft",
            "customer_email": args.get("customer_email"),
            "amount": args.get("amount"),
            "due_date": args.get("due_date"),
        }
        _INVOICES[invoice_id] = invoice
        return _tool_result({"invoice": invoice})
    if name == "crm.send_invoice":
        invoice = _INVOICES.get(str(args.get("invoice_id")), {"id": args.get("invoice_id")})
        invoice["status"] = "sent"
        return _tool_result({"invoice": invoice})
    return {
        "content": [{"type": "text", "text": f"unknown tool: {name}"}],
        "isError": True,
    }


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        method = message.get("method")
        if method == "initialize":
            result: dict[str, Any] = {
                "protocolVersion": "2025-06-18",
                "serverInfo": {"name": "mock-crm", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {"name": "crm.create_invoice", "description": "Create a draft invoice"},
                    {"name": "crm.send_invoice", "description": "Send an invoice"},
                ]
            }
        elif method == "tools/call":
            result = _handle_call(message.get("params") or {})
        else:
            continue
        response = {"jsonrpc": "2.0", "id": message.get("id"), "result": result}
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
