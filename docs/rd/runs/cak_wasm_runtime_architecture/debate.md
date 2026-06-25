# Debate - CAK WASM Runtime Architecture

## Position A: Replace core with WASM

Argument:

- One portable artifact could run in many environments.

Objection:

- The current core is already host-neutral, pure, and small. Replacing it adds
  a runtime dependency and ABI complexity without solving the immediate product
  problem.

Verdict: reject for v0.

## Position B: Use WASM for custom evaluator plugins

Argument:

- WASM is a strong containment and artifact boundary for untrusted executable
  extensions.
- It fits lifecycle, provenance, hash, replay, and rollback better than
  Python/shell scripts.

Objection:

- Tooling and ABI design can get ahead of CAK's skill semantics.

Verdict: reserve and test through a spike.

## Position C: Use Python/scripts first

Argument:

- This is easiest for users and matches ordinary skill folder ergonomics.

Objection:

- Scripts are not safe enough for authoritative runtime-control decisions
  without extra sandboxing and dependency controls.

Verdict: allow for advisory/dev helper paths, not as authoritative evaluator
default.

## Position D: Defer executable evaluators entirely

Argument:

- The next useful step is still `cak skill init/check/install` for package
  admission. That does not need WASM.

Objection:

- If CAK ignores WASM now, it may paint itself into a package-only corner.

Verdict: adopt immediate deferral, but reserve descriptor vocabulary so the
architecture remains open.

## Judge synthesis

WASM should influence the architecture now, but not the dependency graph. Keep
the pure Rust core, keep ordinary skills simple, and define a future
`wasm_component` lane for promoted executable evaluators.
