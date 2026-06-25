# Claim Matrix - CAK WASM Runtime Architecture

| Claim | Support | Confidence | Used in decision | Limitation |
|---|---|---:|---|---|
| CAK should not replace `cak-runtime-core` with WASM now. | `src_cak_runtime_v0`, `src_cak_core_source`, provider critique | High | Yes | Future browser/edge needs could reopen this. |
| WASM is a strong candidate for sandboxed authoritative custom evaluators. | `src_wasmtime_security`, `src_extism` | High | Yes | Only if CAK actually needs executable untrusted evaluators. |
| WASM does not automatically preserve CAK determinism. | `src_wasmtime_deterministic`, `src_wasmtime_interrupting` | High | Yes | Host config can control much of the risk. |
| Component Model/WIT should not be frozen before the evaluator interface stabilizes. | `src_component_model`, provider critique | Medium | Yes | A JSON-string ABI can become technical debt if kept too long. |
| Ordinary custom skills should not require WASM compilation. | `src_runtime_skill_scope`, custom-skill lab direction | High | Yes | Promoted authoritative code may need stronger packaging. |
| A separate `cak-wasm-runner` spike can test the option without weakening the core. | CAK workspace layout, Wasmtime embeddability | Medium | Yes | Spike still needs implementation evidence. |

## Unsupported claims

- WASM will make CAK secure by itself.
- WASM will make custom skill authoring simpler by itself.
- CAK needs Component Model in v0.
- Python/shell scripts are safe enough for authoritative runtime-control skills.
