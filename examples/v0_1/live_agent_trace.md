# v0.1 Live Agent Trace

Date: 2026-06-11

Agent stack: Codex CLI using the CAK gateway as an MCP stdio server.

Repository MCP config: `.mcp.json` is copied from
`examples/v0_1/mcp_config_example.json`. For this Codex CLI run, the same
gateway command was registered under MCP server name `cak_crm` because Codex
CLI stores MCP servers in TOML rather than `.mcp.json`.

Gateway command:

```sh
python3 -m cak.gateway \
  --config examples/v0_1/gateway_config.json \
  --identity billing-agent \
  --trace .cak/trace.jsonl \
  --approvals .cak/approvals \
  -- python3 examples/v0_1/mock_crm_server.py
```

Operator approval:

```sh
PYTHONPATH=src python3 -m cak.approve \
  --store .cak/approvals \
  grant 8d611715fd53 \
  --approver vi
```

Flow captured in `live_agent_trace.jsonl`:

- `amount=500` -> `allow`, invoice created, postconditions checked.
- `amount=20000` -> typed denial with approval request `8d611715fd53`.
- Operator grants `8d611715fd53`.
- Identical retry of `amount=20000` -> approval consumed, invoice created,
  postconditions checked.
- Repeating `amount=20000` without a new grant -> typed denial with approval
  request `776455bf78ec`.
- `amount=-5` -> blocked by precondition `amount > 0`.

Verification:

- Trace events: 17.
- Proposals: 5.
- Decisions checked by replay: 5.
- Postcondition sets checked by replay: 2.
- Replay result: ok, no divergences.
