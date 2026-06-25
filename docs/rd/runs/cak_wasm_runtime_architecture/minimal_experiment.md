# Minimal Experiment - CAK WASM Runtime Architecture

Status: not run.

## Goal

Test whether a separate WASM runner can execute admitted CAK evaluator plugins
without changing `cak-runtime-core`.

## Proposed crate

```text
crates/cak-wasm-runner/
```

It should be experimental and optional.

## Candidate ABI

Start with the current JSON contract:

```text
evaluate(request_json: string) -> decision_json: string
```

Defer full WIT records until the evaluator interface stabilizes.

## Sandbox defaults

- no default WASI;
- no filesystem;
- no network;
- no environment access;
- deterministic fuel;
- memory limit;
- captured stdout/stderr;
- artifact hash recorded.

## Steps

1. Build a trivial Rust WASM guest evaluator.
2. Run one allow fixture and one block fixture through the WASM runner.
3. Compare output against native fixture expected JSON.
4. Add an infinite loop guest and verify deterministic fuel trap.
5. Add a denied I/O attempt if any WASI surface is enabled.
6. Record cold/warm latency.
7. Record `cak` binary size impact.
8. Record artifact hash and rollback metadata in a temp registry.

## Acceptance criteria

- `cak-runtime-core` remains unchanged.
- WASM runner emits valid `Decision` JSON for fixture requests.
- Deterministic replay passes.
- Infinite loop is trapped.
- No ambient I/O is available.
- Latency and binary-size impact are acceptable enough for CLI distribution.

## Kill criteria

- The spike needs changes to the pure core.
- Deterministic fixture replay is not stable.
- Wasmtime/Extism dependency impact is too large for install/update UX.
- Guest authoring requires too much manual toolchain work.
- WASM adds no practical value over native Rust built-ins plus package
  admission.
