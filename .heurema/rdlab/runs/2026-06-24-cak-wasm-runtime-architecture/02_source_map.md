# 02 Source Map

This source map records the inspected internal and external sources used to
decide the WASM runtime direction.

## Project config sources

| Source ID | Source | Mode | Trust | Watch | Status |
|---|---|---|---|---|---|
| cfg_rdlab | `.heurema/rdlab/rdlab.toml` | inspected | project config | no | used |
| cfg_providers | `.heurema/rdlab/providers.toml` | inspected/probed | project config | no | used |

## Primary sources

| Priority | Source | Mode | Why it matters | Status |
|---|---|---|---|---|
| P0 | `docs/22_cak_runtime_v0.md` | inspected | Current runtime boundary and non-goals | used |
| P0 | `crates/cak-runtime-core/src/lib.rs` | inspected | Enforced purity/no-I/O invariant | used |
| P0 | `docs/rd/runs/rdr_001_agent_native_skill/programmatic_runtime_skill_scope.md` | inspected | Distinguishes packages from runtime-control skills | used |
| P0 | Wasmtime docs | inspected | WASM runtime, sandbox, determinism, interruption | used |
| P0 | WASI docs | inspected | Capability APIs, maturity, proposal status | used |
| P0 | Component Model docs | inspected | WIT/interfaces/worlds as typed plugin ABI | used |
| P1 | Extism docs | inspected | Pragmatic WASM plugin framework option | used |

## External source pass

| Priority | Source | Mode | What it can support | Status |
|---|---|---|---|---|
| P0 | Wasmtime introduction | raw GitHub docs | Wasmtime is embeddable, secure/configurable, supports WASI and Component Model | used |
| P0 | Wasmtime security | raw GitHub docs | WASM sandbox properties, imports/exports, WASI capability filesystem, terminal output hazards | used |
| P0 | Wasmtime deterministic execution | raw GitHub docs | Determinism requires deterministic imports, NaN/SIMD settings, memory/table handling, fuel | used |
| P0 | Wasmtime interrupting execution | raw GitHub docs | Fuel is deterministic but slower; epoch interruption is faster but non-deterministic | used |
| P0 | Component Model introduction/design docs | raw GitHub docs | Components are self-describing, typed, WIT-based, cross-language ABI | used |
| P0 | WASI README/proposals | raw GitHub docs | WASI 0.2/0.3 status and proposal maturity | used |
| P1 | Extism README/Rust PDK | raw GitHub docs | WebAssembly plugin framework and simple exported function workflow | used |

## Sources to avoid or treat carefully

| Source | Reason |
|---|---|
| Provider outputs | Useful as critique only; not source evidence about WASM specs. |
| Unloaded Wasmtime HTML pages | Timed out in this environment; not used as evidence. |
