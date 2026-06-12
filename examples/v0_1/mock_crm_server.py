"""Mock CRM MCP server (stdio, newline-delimited JSON-RPC) for the v0.1 demo.

Implements just enough of MCP: initialize, tools/list, tools/call for
crm.create_invoice and crm.send_invoice. State is in-memory.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from cak.mcp_stdio import read_message, write_message

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
    if name == "crm.void_invoice":
        invoice = _INVOICES.get(str(args.get("invoice_id")), {"id": args.get("invoice_id")})
        invoice["status"] = "void"
        return _tool_result({"invoice": invoice})
    return {
        "content": [{"type": "text", "text": f"unknown tool: {name}"}],
        "isError": True,
    }


def main() -> None:
    while True:
        envelope = read_message(sys.stdin.buffer)
        if envelope is None:
            return
        if not envelope.payload.strip():
            continue
        message = json.loads(envelope.payload)
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
                    {
                        "name": "crm.create_invoice",
                        "description": "Create a draft invoice",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "customer_email": {"type": "string"},
                                "amount": {"type": "number"},
                                "due_date": {"type": "string"},
                            },
                            "required": ["customer_email", "amount", "due_date"],
                            "additionalProperties": False,
                        },
                    },
                    {
                        "name": "crm.send_invoice",
                        "description": "Send an invoice",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"invoice_id": {"type": "string"}},
                            "required": ["invoice_id"],
                            "additionalProperties": False,
                        },
                    },
                    {
                        "name": "crm.void_invoice",
                        "description": "Void an invoice (compensation)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"invoice_id": {"type": "string"}},
                            "required": ["invoice_id"],
                            "additionalProperties": False,
                        },
                    },
                ]
            }
        elif method == "tools/call":
            result = _handle_call(message.get("params") or {})
        elif method == "resources/list":
            result = {"resources": []}
        elif method == "resources/templates/list":
            result = {"resourceTemplates": []}
        elif method == "prompts/list":
            result = {"prompts": []}
        else:
            continue
        response = {"jsonrpc": "2.0", "id": message.get("id"), "result": result}
        write_message(sys.stdout.buffer, response, framed=envelope.framed)


if __name__ == "__main__":
    main()
