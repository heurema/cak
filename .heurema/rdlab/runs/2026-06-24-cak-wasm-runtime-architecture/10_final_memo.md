# 10 Final Memo

## Executive summary

WASM was not considered earlier because the prior runs were about install UX
and ordinary custom skill packaging. WASM is not primarily an install UX; it is
a sandboxed execution/ABI option for untrusted executable runtime extensions.

Verdict:

- Do not replace `cak-runtime-core` with WASM.
- Keep the Rust core as the authoritative pure `EvalRequest -> Decision`
  engine.
- Reserve WASM as a future optional plugin/evaluator ABI for promoted,
  authoritative custom runtime-control skills.
- Before implementing it, run a separate `cak-wasm-runner` spike with fuel,
  memory limits, no default WASI, fixture replay, artifact hashes, and rollback
  metadata.

## Why this matters

If CAK later lets users write executable evaluators, Python or shell scripts are
simple but weak for containment and rollback. WASM is a plausible promotion path
for those evaluators because it is sandboxed by imports/exports and can be
artifact-hashed, replayed, and rolled back.

## What changes now

Only the architecture vocabulary should change now:

```text
package          ordinary SKILL.md host package
script           local helper/advisory code, not authoritative by default
wasm_component   future sandboxed executable evaluator/intervention candidate
```

Do not add Wasmtime/Extism to the repo until the spike is approved.

## Recommended decision

Decision-ready for direction:

```text
Keep Rust core.
Reserve WASM extension point.
Run optional spike before authoritative custom evaluator support.
```

Implementation-ready: no.

## Decision log entry

```text
Date: 2026-06-24
Project: CAK
Decision: Do not replace the Rust CAK runtime core with WASM; reserve WASM as a future optional sandboxed evaluator ABI and validate it through a separate runner spike.
Reason: WASM addresses untrusted executable extension containment, not the current core runtime problem. The existing Rust core is smaller, deterministic, and already matches EvalRequest -> Decision.
What this prevents: Premature Wasmtime dependency, Component Model ABI lock-in, making ordinary custom skills harder, and weakening the pure-core invariant.
Review date: After cak skill init/check/install exists and a temp-dir cak-wasm-runner spike measures DX, latency, binary size, deterministic replay, and rollback.
```
