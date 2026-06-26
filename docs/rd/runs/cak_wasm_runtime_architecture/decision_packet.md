# Decision Packet - CAK WASM Runtime Architecture

Status: decision-ready for architecture direction; not implementation-ready.

## Decision

Do not use WASM as the CAK core runtime now.

Adopt this architecture direction:

```text
Rust core remains authoritative and pure.
WASM is reserved as a future optional sandboxed evaluator ABI.
Ordinary custom skills remain SKILL.md + cak.yaml packages.
```

## Why WASM was not considered earlier

The previous discussions were about install/update UX and simple custom skill
authoring. WASM is a different layer: it is an execution sandbox and ABI for
untrusted executable code. It becomes relevant only when CAK allows user-authored
runtime-control evaluators or interventions, not for ordinary skill folders.

## What this changes

The architecture vocabulary should leave room for future runtime kinds:

```yaml
runtime:
  kind: package        # ordinary host skill package
  # kind: script       # advisory/local helper, not authoritative by default
  # kind: wasm_component # future sandboxed executable evaluator
```

Do not add Wasmtime or Extism to `cak-runtime-core`.

## What this rejects

- Replacing `cak-runtime-core` with WASM.
- Making all custom skills compile to WASM.
- Freezing a Component Model/WIT ABI before CAK proves evaluator semantics.
- Treating Python/shell scripts as safe authoritative policy plugins.
- Enabling broad WASI capabilities by default.

## Quality gate

Decision-ready for direction: pass.

Reasons:

- current CAK core boundary and dependency surface were inspected;
- official Wasmtime security/determinism/interruption docs were inspected;
- official WASI and Component Model docs were inspected;
- Extism was inspected as a practical plugin-framework option;
- provider critique produced both positive and negative WASM arguments;
- minimal experiment and kill criteria are specified.

Implementation-ready: fail.

Blockers:

- no `cak-wasm-runner` spike;
- no measured binary size impact;
- no latency numbers;
- no multi-language guest build attempt;
- no hostile plugin tests;
- no final WIT or JSON ABI decision.

## Next step

Proceed first with ordinary custom skill UX:

```sh
cak skill init
cak skill check
cak skill install
```

Then run the optional WASM spike before promoting any custom executable
evaluator to authoritative status.
