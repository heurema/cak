# Research Plan - CAK WASM Runtime Architecture

## Research question

Should CAK use WebAssembly/WASI/Component Model as its runtime architecture now
that custom skill authoring and distribution are being designed?

## Scope

- WASM as replacement for the Rust `cak-runtime-core`.
- WASM as sandboxed plugin/evaluator ABI.
- WASM as deferred optional extension.
- Determinism, resource limits, capability control, artifact provenance, and
  rollback.
- User-created skills and future authoritative runtime-control evaluators.

## Non-goals

- Implementing Wasmtime, Extism, or Component Model support now.
- Public package registry.
- Browser runtime support.
- Full hostile-code security audit.
- Final WIT schema.

## Source strategy

Use current CAK runtime docs and official WebAssembly ecosystem sources:

- current CAK runtime docs and source;
- Wasmtime introduction, security, deterministic execution, and interruption
  docs;
- WASI README/proposal docs;
- Component Model/WIT docs;
- Extism plugin docs as a pragmatic plugin-framework example;
- rdlab provider passes as critique only.

## Expected counterarguments

- WASM gives CAK a stronger sandbox for untrusted custom evaluators.
- WASM adds dependency size and ABI complexity before CAK knows what custom
  runtime-control skills need.
- Component Model/WIT is the right long-term typed ABI, but JSON is simpler
  while the schema is moving.
- Python/script custom skills are easier for users, but weaker for
  authoritative containment.

## Minimal experiment candidate

Build a separate optional `cak-wasm-runner` spike. Do not change
`cak-runtime-core`. Run one Rust guest evaluator over existing fixtures with no
default WASI, deterministic fuel, memory limit, artifact hash, and rollback
metadata.

## Stop rules

Stop before implementation if:

- the experiment requires changing `cak-runtime-core`;
- deterministic replay cannot be guaranteed;
- binary size or latency breaks install/update UX;
- guest toolchain setup is too hard for intended users;
- WASM does not add value over native Rust evaluators plus package admission.
