# 04 Change Log

## 2026-06-24

- Created project-local rdlab run for WASM runtime architecture.
- Probed provider routes: Claude, Vibe, and Agy available.
- Inspected internal CAK runtime docs, core source, workspace dependencies, and
  RDR-001 runtime-skill scope gate.
- Inspected official Wasmtime, WASI, Component Model/WIT, and Extism docs.
- Ran provider passes:
  - Agy returned a useful synthesis: reject core replacement, consider WASM as
    plugin ABI later.
  - Claude-haiku returned a useful critique: avoid ABI lock-in before skill
    semantics are proven.
  - Vibe returned a stop event without content.
- Drafted recommendation: keep Rust core, reserve optional WASM plugin ABI, run
  a separate spike before authoritative custom evaluators.
