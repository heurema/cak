"""MCP stdio gateway: the credential-owning enforcement point (docs/13).

Form factor:

    agent (MCP client) -> this proxy -> upstream MCP server

The proxy spawns the upstream server itself, so upstream credentials live in
the gateway environment, not in the agent process (docs/11: enforcement is
real only when the kernel owns the tool boundary). `tools/call` requests are
verified before forwarding; everything else passes through. Denials are
answered with a typed, replayable audit object instead of a tool result.

v0.1 approval semantics: `require_approval` denies the call and records the
decision; interactive approval flows are out of scope for the skeleton.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

from .predicates import evaluate_all
from .specs import GatewayConfig, load_config_file
from .trace import TraceRecorder
from .verifier import Proposal, verify


@dataclass(slots=True)
class _PendingCall:
    action: str
    effect_id: str | None


class Gateway:
    def __init__(
        self,
        config: GatewayConfig,
        identity: str,
        recorder: TraceRecorder,
        upstream_in: IO[bytes],
        upstream_out: IO[bytes],
        client_in: IO[bytes],
        client_out: IO[bytes],
    ) -> None:
        self._config = config
        self._identity = identity
        self._recorder = recorder
        self._upstream_in = upstream_in
        self._upstream_out = upstream_out
        self._client_in = client_in
        self._client_out = client_out
        self._pending: dict[Any, _PendingCall] = {}
        self._write_lock = threading.Lock()

    # -- transport helpers -------------------------------------------------

    def _send(self, stream: IO[bytes], message: dict[str, Any]) -> None:
        data = json.dumps(message, ensure_ascii=False).encode("utf-8") + b"\n"
        with self._write_lock:
            stream.write(data)
            stream.flush()

    # -- client -> upstream ------------------------------------------------

    def _deny(self, message: dict[str, Any], decision_dict: dict[str, Any]) -> None:
        denial = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            {"cak_denial": decision_dict}, ensure_ascii=False
                        ),
                    }
                ],
            },
        }
        self._send(self._client_out, denial)

    def handle_client_message(self, line: bytes) -> None:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            self._upstream_in.write(line)
            self._upstream_in.flush()
            return

        if not (isinstance(message, dict) and message.get("method") == "tools/call"):
            self._send(self._upstream_in, message)
            return

        params = message.get("params") or {}
        action = str(params.get("name", ""))
        arguments_raw = params.get("arguments") or {}
        arguments: dict[str, Any] = arguments_raw if isinstance(arguments_raw, dict) else {}
        call_id = message.get("id")

        self._recorder.proposal(call_id, self._identity, action, arguments)
        decision = verify(self._config, Proposal(self._identity, action, arguments))
        decision_dict = decision.to_dict()
        self._recorder.decision(call_id, decision_dict)

        if decision.enforcement in {"block", "require_approval"}:
            self._deny(message, decision_dict)
            return

        self._pending[call_id] = _PendingCall(action, decision.effect_id)
        self._send(self._upstream_in, message)

    # -- upstream -> client ------------------------------------------------

    @staticmethod
    def _result_context(result: dict[str, Any]) -> dict[str, Any] | None:
        structured = result.get("structuredContent")
        if isinstance(structured, dict):
            return structured
        content = result.get("content")
        if isinstance(content, list) and content:
            first = content[0]
            if isinstance(first, dict) and first.get("type") == "text":
                try:
                    parsed = json.loads(first.get("text", ""))
                except json.JSONDecodeError:
                    return None
                return parsed if isinstance(parsed, dict) else None
        return None

    def handle_upstream_message(self, line: bytes) -> None:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            self._client_out.write(line)
            self._client_out.flush()
            return

        call_id = message.get("id") if isinstance(message, dict) else None
        pending = self._pending.pop(call_id, None)
        if pending is not None:
            result = message.get("result")
            error = message.get("error")
            self._recorder.outcome(
                call_id,
                result if isinstance(result, dict) else None,
                error if isinstance(error, dict) else None,
            )
            effect = self._config.effects_by_action.get(pending.action)
            if effect is not None and effect.causes and isinstance(result, dict):
                context = self._result_context(result)
                checks = {
                    predicate: truth.value
                    for predicate, truth in evaluate_all(
                        list(effect.causes), context or {}
                    ).items()
                }
                self._recorder.postconditions(call_id, effect.id, checks, context)

        self._send(self._client_out, message)

    # -- pumps ---------------------------------------------------------------

    def _pump_upstream(self) -> None:
        for line in iter(self._upstream_out.readline, b""):
            if line.strip():
                self.handle_upstream_message(line)

    def run(self) -> None:
        thread = threading.Thread(target=self._pump_upstream, daemon=True)
        thread.start()
        for line in iter(self._client_in.readline, b""):
            if line.strip():
                self.handle_client_message(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CAK v0.1 MCP gateway proxy")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--identity", required=True)
    parser.add_argument("--trace", required=True, type=Path)
    parser.add_argument("upstream", nargs=argparse.REMAINDER,
                        help="-- upstream MCP server command")
    args = parser.parse_args(argv)

    upstream_cmd = [part for part in args.upstream if part != "--"]
    if not upstream_cmd:
        parser.error("upstream MCP server command is required after --")

    config = load_config_file(args.config)
    recorder = TraceRecorder(args.trace)

    process = subprocess.Popen(
        upstream_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    assert process.stdin is not None and process.stdout is not None

    gateway = Gateway(
        config=config,
        identity=args.identity,
        recorder=recorder,
        upstream_in=process.stdin,
        upstream_out=process.stdout,
        client_in=sys.stdin.buffer,
        client_out=sys.stdout.buffer,
    )
    try:
        gateway.run()
    finally:
        process.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
