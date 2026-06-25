# Hypothesis Matrix - CAK WASM Runtime Architecture

| Hypothesis | Description | Supports | Weaknesses | Minimal experiment | Verdict |
|---|---|---|---|---|---|
| H1: WASM replaces Rust core | Compile or run the CAK decision core through WASM. | Maximum theoretical portability. | Adds runtime dependency, debugging cost, ABI surface, and no clear benefit over current pure Rust core. | Port current evaluators to WASM and compare fixtures. | Reject for v0. |
| H2: WASM as sandboxed plugin/evaluator ABI | Keep Rust core; load admitted WASM evaluators from a separate runner. | Strong containment, artifact hashing, rollback, polyglot future. | Tooling and ABI complexity; needs deterministic host config and UX proof. | `cak-wasm-runner` spike. | Reserve and experiment. |
| H3: Scripts/subprocesses as evaluator ABI | Let users write Python/shell/JS evaluators over JSON stdin/stdout. | Easiest authoring. | Weak containment, dependency drift, hard rollback, unsafe for authority. | Temp-dir script runner with fixtures. | Advisory/dev only; not authoritative default. |
| H4: Native Rust-only custom evaluators | Add Rust evaluator crates/plugins. | Best fit with current core, strong types. | Not simple for users, limited polyglot extension. | Add one native evaluator crate. | Keep for built-ins; not enough for user extensibility. |
| H5: Defer all executable evaluators | Only ordinary `SKILL.md` + `cak.yaml` package admission for now. | Simple, preserves current architecture. | Does not solve future executable intervention use cases. | Custom skill init/check/install experiment. | Adopt for immediate v0. |

## Selected direction

Use H5 immediately. Reserve H2 in architecture and run H2 only as a bounded
spike before allowing authoritative user-authored executable evaluators.
