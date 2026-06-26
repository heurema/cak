# 07 Ideas

## Descriptor shape to reserve

```yaml
id: local.demo-evaluator
version: 0.1.0
kind: verifier

runtime:
  kind: wasm_component
  artifact: target/wasm32-wasip2/release/demo_evaluator.wasm
  abi: heurema:cak/evaluator@0.1.0
  entrypoint: evaluate

sandbox:
  wasi: none
  fuel: 1000000
  memory_max_bytes: 16777216
  network: false
  filesystem: []

admission:
  maturity: draft
  required_fixtures:
    - fixtures/allow.request.json
    - fixtures/block.request.json
```

## First ABI idea

Use JSON strings first to preserve the current contract:

```text
evaluate(request_json: string) -> result<decision_json: string, error: string>
```

Only move to full WIT records when the `EvalRequest`/`Decision` schema has
enough stability and non-Rust binding quality matters.

## Runner placement

```text
crates/cak-runtime-core/       pure, unchanged
crates/cak-wasm-runner/        optional experiment, embeds Wasmtime/Extism
crates/cak-runtime-cli/        may call runner behind experimental command
```

## Possible commands

```sh
cak wasm check ./demo-evaluator
cak wasm run --request fixtures/allow.request.json ./demo-evaluator.wasm
cak skill check ./demo-evaluator
cak skill install ./demo-evaluator --experimental-wasm
```

Do not expose these as stable commands until the spike passes.
