# 06 Synthesis

## What is known

- CAK's current Rust core is small, deterministic, and pure.
- Wasmtime provides an embeddable WebAssembly/WASI/Component Model runtime.
- Wasmtime's sandbox model is relevant to untrusted custom code because a
  module can only interact with host-provided imports/exports.
- WASI uses capabilities, including capability-scoped filesystem access.
- Deterministic WASM execution requires careful host/import/config choices.
- Component Model/WIT gives a typed, cross-language ABI, but it is heavier than
  CAK's current JSON contract.
- Extism provides a practical plugin framework and PDK, useful for a spike.

## What is uncertain

- Whether CAK actually needs user-authored executable runtime evaluators in v0.
- Whether target users can tolerate WASM toolchain setup.
- Whether a Wasmtime/Extism dependency is acceptable for the `cak` CLI binary
  size and install/update UX.
- Whether JSON-string ABI is sufficient or WIT should be first-class.

## Patterns

- Keep the core pure and host-neutral.
- Treat WASM as an isolation boundary for executable extensions, not as the
  product runtime itself.
- Use deterministic fuel for replay/admission tests.
- Default to no WASI. Add specific host imports only after they are justified.
- Record WASM artifact hash, ABI version, fuel/memory limits, source provenance,
  fixture pass state, and rollback checkpoint.

## Anti-patterns

- Replacing `cak-runtime-core` with WASM before proving the need.
- Treating WASM as automatically deterministic.
- Giving plugins broad WASI filesystem/network access.
- Making ordinary custom skill authors compile WASM before they can start.
- Designing a WIT ABI before the evaluator interface stabilizes.

## Architecture options

### A: WASM replaces the Rust core

Reject for now. It adds an embedded runtime/dependency layer to solve a problem
the current Rust core does not have.

### B: WASM is a sandboxed plugin/evaluator ABI

Promising, but not implementation-ready. Best fit for promoted, authoritative,
executable runtime-control skills.

### C: WASM is deferred but reserved in descriptors

Recommended. Keep ordinary skills simple now, but avoid closing the architecture
by reserving `runtime.kind = wasm_component` / `wasm_plugin` in future
`cak.yaml` schema discussions.

## Strategic implication

The architecture should change slightly now: not by adding Wasmtime, but by
separating custom skill classes:

- `package`: ordinary `SKILL.md` host package, not authoritative runtime code;
- `script`: local helper or advisory script, not trusted for authoritative
  policy unless externally gated;
- `wasm_component`: future sandboxed evaluator/intervention candidate.

## Recommended experiment

Timebox a separate `cak-wasm-runner` spike after `cak skill init/check/install`
exists. The spike should be temp-dir only and should not touch
`cak-runtime-core`.
