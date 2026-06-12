"""MCP stdio gateway: the credential-owning enforcement point (docs/13).

Form factor:

    agent (MCP client) -> this proxy -> upstream MCP server

The proxy spawns the upstream server itself, so upstream credentials live in
the gateway environment, not in the agent process (docs/11: enforcement is
real only when the kernel owns the tool boundary). `tools/call` requests are
verified before forwarding; everything else passes through. Denials are
answered with a typed, replayable audit object instead of a tool result.

Approval semantics (docs/07, docs/18): `require_approval` checks the approval
store for a valid single-use token scoped to this exact call (identity +
action + args hash). With a token the call is forwarded and the consumption
is traced; without one a typed denial is returned carrying a queued approval
request id for `python -m cak.approve`.

Compensation semantics (docs/19): when a compensable effect completes, the
gateway derives the compensating call from the typed CompensationSpec and
traces it as `compensation_prepared`; a postcondition failure adds
`compensation_suggested`. Nothing auto-fires — when the agent (or operator)
issues the prepared call, it passes the verifier like any action and its
success is traced as `compensation_executed`, linking the saga chain.
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

from .approvals import ApprovalStore, args_hash
from .mcp_stdio import read_message, write_message
from .predicates import evaluate_all
from .specs import CompensationSpec, GatewayConfig, load_config_file
from .trace import TraceRecorder
from .verifier import Proposal, verify


@dataclass(slots=True)
class _PendingCall:
    action: str
    effect_id: str | None
    arguments: dict[str, Any]
    compensates_call_id: Any = None


def _dig(context: dict[str, Any], dotted: str) -> tuple[bool, Any]:
    node: Any = context
    for part in dotted.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return False, None
    return True, node


def _derive_compensation(
    spec: CompensationSpec,
    arguments: dict[str, Any],
    result_context: dict[str, Any],
) -> dict[str, Any] | None:
    """Resolve compensation arguments; None when any path is unresolvable."""
    derived: dict[str, Any] = {}
    for param, path in spec.args_from_result.items():
        found, value = _dig(result_context, path)
        if not found:
            return None
        derived[param] = value
    for param, path in spec.args_from_args.items():
        found, value = _dig(arguments, path)
        if not found:
            return None
        derived[param] = value
    return derived


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
        approvals: ApprovalStore | None = None,
    ) -> None:
        self._config = config
        self._identity = identity
        self._recorder = recorder
        self._approvals = approvals
        self._upstream_in = upstream_in
        self._upstream_out = upstream_out
        self._client_in = client_in
        self._client_out = client_out
        self._pending: dict[Any, _PendingCall] = {}
        # (action, args_hash) -> call_id of the completed call it compensates.
        self._prepared_compensations: dict[tuple[str, str], Any] = {}
        self._client_framed = False
        self._write_lock = threading.Lock()

    # -- transport helpers -------------------------------------------------

    def _send(
        self, stream: IO[bytes], message: dict[str, Any], framed: bool
    ) -> None:
        with self._write_lock:
            write_message(stream, message, framed=framed)

    # -- client -> upstream ------------------------------------------------

    def _deny(
        self,
        message: dict[str, Any],
        decision_dict: dict[str, Any],
        extra: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {"cak_denial": decision_dict, **(extra or {})}
        denial = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(payload, ensure_ascii=False),
                    }
                ],
            },
        }
        self._send(self._client_out, denial, framed=self._client_framed)

    def handle_client_message(self, payload: bytes, framed: bool) -> None:
        self._client_framed = framed
        try:
            message = json.loads(payload)
        except json.JSONDecodeError:
            self._upstream_in.write(payload)
            if not framed:
                self._upstream_in.write(b"\n")
            self._upstream_in.flush()
            return

        if not (isinstance(message, dict) and message.get("method") == "tools/call"):
            self._send(self._upstream_in, message, framed=framed)
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

        if decision.enforcement == "block":
            self._deny(message, decision_dict)
            return

        if decision.enforcement == "require_approval":
            token = (
                self._approvals.consume(self._identity, action, arguments)
                if self._approvals is not None
                else None
            )
            if token is None:
                extra: dict[str, Any] = {}
                if self._approvals is not None:
                    request_id = self._approvals.request(
                        self._identity, action, arguments, decision_dict
                    )
                    self._recorder.emit(
                        "approval_requested",
                        {"call_id": call_id, "request_id": request_id},
                    )
                    extra = {
                        "approval_request_id": request_id,
                        "retry_after_approval": True,
                    }
                self._deny(message, decision_dict, extra)
                return
            self._recorder.emit(
                "approval_consumed",
                {
                    "call_id": call_id,
                    "request_id": token["request_id"],
                    "approved_by": token["approved_by"],
                    "expires_at": token["expires_at"],
                    "args_hash": token["args_hash"],
                },
            )

        compensates = self._prepared_compensations.pop(
            (action, args_hash(arguments)), None
        )
        self._pending[call_id] = _PendingCall(
            action, decision.effect_id, arguments, compensates
        )
        self._send(self._upstream_in, message, framed=framed)

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

    def handle_upstream_message(self, payload: bytes) -> None:
        try:
            message = json.loads(payload)
        except json.JSONDecodeError:
            self._client_out.write(payload)
            if not self._client_framed:
                self._client_out.write(b"\n")
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
            context: dict[str, Any] | None = None
            checks: dict[str, str] = {}
            if effect is not None and effect.causes and isinstance(result, dict):
                context = self._result_context(result)
                checks = {
                    predicate: truth.value
                    for predicate, truth in evaluate_all(
                        list(effect.causes), context or {}
                    ).items()
                }
                self._recorder.postconditions(call_id, effect.id, checks, context)

            prepared: dict[str, Any] | None = None
            if (
                effect is not None
                and effect.compensation is not None
                and error is None
                and context is not None
            ):
                derived = _derive_compensation(
                    effect.compensation, pending.arguments, context
                )
                if derived is not None:
                    prepared = {
                        "action": effect.compensation.action,
                        "arguments": derived,
                    }
                    self._prepared_compensations[
                        (effect.compensation.action, args_hash(derived))
                    ] = call_id
                    self._recorder.emit(
                        "compensation_prepared",
                        {"call_id": call_id, "effect_id": effect.id, **prepared},
                    )

            failed = [predicate for predicate, truth in checks.items() if truth == "false"]
            if failed:
                self._recorder.emit(
                    "compensation_suggested",
                    {
                        "call_id": call_id,
                        "failed_postconditions": failed,
                        "compensation": prepared,
                    },
                )

            if pending.compensates_call_id is not None and error is None:
                self._recorder.emit(
                    "compensation_executed",
                    {
                        "call_id": call_id,
                        "compensates_call_id": pending.compensates_call_id,
                    },
                )

        self._send(self._client_out, message, framed=self._client_framed)

    # -- pumps ---------------------------------------------------------------

    def _pump_upstream(self) -> None:
        while True:
            message = read_message(self._upstream_out)
            if message is None:
                return
            if message.payload.strip():
                self.handle_upstream_message(message.payload)

    def run(self) -> None:
        thread = threading.Thread(target=self._pump_upstream, daemon=True)
        thread.start()
        while True:
            message = read_message(self._client_in)
            if message is None:
                return
            if message.payload.strip():
                self.handle_client_message(message.payload, framed=message.framed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CAK v0.1 MCP gateway proxy")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--identity", required=True)
    parser.add_argument("--trace", required=True, type=Path)
    parser.add_argument("--approvals", type=Path, default=None,
                        help="approval store directory (enables approval tokens)")
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
        approvals=ApprovalStore(args.approvals) if args.approvals else None,
    )
    try:
        gateway.run()
    finally:
        process.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
