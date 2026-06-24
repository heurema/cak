---
name: cak-host-adapter
description: Run the Rust CAK host adapter gate from an Agent-Skills-compatible wrapper.
---

# CAK Host Adapter

This skill is a thin launcher for the Rust host adapter. It does not implement
policy logic in Python. The script calls:

```sh
cakrt gate --proposal <proposal.json>
```

The proposal JSON currently uses the same shape as `EvalRequest`; the Rust
adapter maps the runtime `Decision` to a host-facing outcome before any host
executes the proposed action.
