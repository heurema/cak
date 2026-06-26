# 05 Contradictions

## C1: Strong sandbox vs simple custom skill UX

WASM is attractive for untrusted executable extensions, but compiling to WASM
is much harder than editing an ordinary `SKILL.md`.

Resolution: do not require WASM for ordinary custom skills. Use it only for a
future promoted class of authoritative executable evaluators.

## C2: Portable plugin ABI vs current pure Rust core

Embedding Wasmtime in `cak-runtime-core` would weaken the current small,
pure dependency boundary.

Resolution: keep core pure. If tested, put WASM in a separate optional runner
crate or CLI path.

## C3: WASM determinism claim vs actual host configuration

WASM is mostly deterministic, but imports, NaN values, relaxed SIMD,
memory/table growth, and interruption mode can introduce nondeterminism.

Resolution: any CAK WASM runner must default to no WASI, deterministic fuel,
explicit memory limits, deterministic Wasmtime config, and replay fixtures.

## C4: Component Model long-term fit vs short-term friction

Component Model/WIT is the better typed ABI story, but it adds design and
tooling work before CAK knows the exact custom evaluator interface.

Resolution: spike a JSON-string ABI first if needed; only promote to WIT after
the evaluator contract stabilizes.

## C5: Provider disagreement

Agy saw WASM as an ideal plugin ABI target; Claude-haiku warned against choosing
WASM before CAK knows what skill abstraction needs.

Resolution: both can be true. Reserve the extension point now; defer dependency
and implementation until a spike proves need.
