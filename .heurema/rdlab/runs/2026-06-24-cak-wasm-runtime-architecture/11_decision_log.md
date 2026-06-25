# 11 Decision Log

```text
Date: 2026-06-24
Project: CAK
Decision: Do not replace the Rust CAK runtime core with WASM; reserve WASM as a future optional sandboxed evaluator ABI and validate it through a separate runner spike.
Reason: WASM addresses untrusted executable extension containment, not the current core runtime problem. The existing Rust core is smaller, deterministic, and already matches EvalRequest -> Decision.
What this prevents: Premature Wasmtime dependency, Component Model ABI lock-in, making ordinary custom skills harder, and weakening the pure-core invariant.
Review date: After cak skill init/check/install exists and a temp-dir cak-wasm-runner spike measures DX, latency, binary size, deterministic replay, and rollback.
```
