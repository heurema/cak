# 01 Question Graph

## Root question

Should CAK use WASM as its runtime before the architecture stabilizes?

## Sub-questions

- Q1: Does WASM improve the current Rust core?
- Q2: Does WASM solve a real problem for custom user skills?
- Q3: Is WASM mature enough as a typed ABI through Component Model/WIT?
- Q4: Can WASM preserve CAK's determinism and audit requirements?
- Q5: What experiment would decide without committing the architecture?

## Current answers

- Q1: No. Replacing the Rust core adds an embedded runtime/dependency layer
  without improving the existing pure `EvalRequest -> Decision` boundary.
- Q2: Yes, but for a narrower capability: sandboxed authoritative custom
  evaluators or interventions, not ordinary `SKILL.md` packages.
- Q3: Promising, but still moving. WASI 0.2 is stable, WASI 0.3 is preview, and
  many APIs are proposal-stage.
- Q4: Possible only with strict host imports, no default WASI, fuel limits,
  memory limits, deterministic settings, and fixture replay.
- Q5: Build a separate optional spike crate, not a core rewrite.

## Decision dependency

Do not decide "WASM runtime" until the project decides whether user-authored
skills can become authoritative runtime-control evaluators.
