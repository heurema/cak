# 08 Experiments

## Minimal experiment: optional WASM evaluator runner

Status: not run.

### Goal

Decide whether WASM should become the promoted executable custom evaluator ABI
for CAK without changing the current Rust core.

### Setup

- Create an experimental crate, `crates/cak-wasm-runner`.
- Do not add Wasmtime/Extism to `cak-runtime-core`.
- Implement one evaluator plugin:
  - Rust guest first;
  - optional TinyGo/JS/Python guest only if toolchain friction is acceptable.

### Candidate ABI

```text
evaluate(request_json: string) -> decision_json: string
```

### Required sandbox settings

- No default WASI.
- No filesystem, network, environment, or clock imports.
- Deterministic fuel interruption.
- Memory limit.
- Captured stdout/stderr or disabled terminal output.
- Artifact hash recorded in admission metadata.

### Steps

1. Build a trivial WASM evaluator that returns `allow`.
2. Build a lifecycle-style evaluator that blocks a quarantined skill fixture.
3. Run the same fixture set through native Rust evaluator and WASM evaluator.
4. Measure cold start and warm evaluation latency.
5. Measure CLI binary size impact.
6. Verify fuel trap on infinite loop fixture.
7. Verify denied filesystem/network attempts if any WASI surface is enabled.
8. Verify rollback can restore the previous WASM artifact hash.

### Acceptance criteria

- `cak-runtime-core` remains unchanged.
- A WASM evaluator can process `EvalRequest` JSON and emit valid `Decision`
  JSON.
- Deterministic replay passes for the same fixture set.
- Infinite loops are stopped by deterministic fuel.
- No filesystem/network access is available by default.
- Binary size and latency stay within a stated budget.
- The authoring/build flow is no more complex than one CAK wrapper command
  after language toolchain installation.

### Kill criteria

- The spike requires changing `cak-runtime-core`.
- The guest cannot produce stable fixture outputs.
- Fuel/memory limits are awkward or unreliable.
- Binary size makes install/update UX materially worse.
- Guest toolchain setup is too hard for the intended custom-skill audience.
- WASM adds no value over native Rust evaluators plus ordinary package
  admission.
