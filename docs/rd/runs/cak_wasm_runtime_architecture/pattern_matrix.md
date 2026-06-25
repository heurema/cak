# Pattern Matrix - CAK WASM Runtime Architecture

| Pattern | Evidence | Fit for CAK | What not to copy | Risk |
|---|---|---|---|---|
| Pure Rust policy kernel | `src_cak_runtime_v0`, `src_cak_core_source` | Strong. Keep as authoritative core. | Do not add plugin execution or I/O into core. | Future custom evaluator flexibility may require a separate runner. |
| WASM import/export sandbox | `src_wasmtime_security` | Strong for untrusted executable evaluators. | Do not treat sandboxing as automatic if host imports are broad. | Misconfigured capabilities can break containment. |
| WASI capability model | `src_wasmtime_security`, `src_wasi` | Useful only if plugins need explicit filesystem/network-like APIs. | Do not enable default WASI for decision evaluators. | Capability creep undermines auditability. |
| Deterministic fuel | `src_wasmtime_interrupting`, `src_wasmtime_deterministic` | Good for replay/admission. | Do not use epoch interruption for deterministic fixture proof. | Fuel overhead must be measured. |
| Component Model/WIT ABI | `src_component_model` | Good long-term typed cross-language ABI. | Do not freeze WIT before CAK's evaluator contract stabilizes. | ABI lock-in and tooling friction. |
| Extism plugin framework | `src_extism` | Good spike candidate for fast plugin proof. | Do not confuse framework convenience with final CAK standard. | Framework dependency may constrain later Component Model direction. |

## Synthesis

WASM is not a better replacement for the current runtime core. It is a better
candidate for one future class of custom skills: sandboxed executable
runtime-control evaluators with explicit admission, fixture replay, provenance,
and rollback.
