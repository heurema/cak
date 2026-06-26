# 00 Spec

## Topic

cak wasm runtime architecture

## Project context

CAK v0 is a Rust workspace with one public CLI, `cak`. The current runtime core
is deliberately small and pure: `EvalRequest` JSON -> `Decision` JSON, no I/O,
no filesystem, no network, no markdown parsing, no script execution, and no LLM
calls. The current custom skill authoring direction keeps ordinary `SKILL.md`
folders and adds CAK metadata through `cak.yaml`.

## Decision context

The user asked why WASM was not considered as the runtime before CAK's
architecture hardens. This run evaluates whether WebAssembly/WASI/Component
Model should replace the Rust core, become the custom evaluator/plugin runtime,
or remain a deferred experiment.

## Intended audience

CAK maintainers deciding the runtime and custom skill admission architecture.

## Output type

Deep research lab run plus decision packet. Docs-only; no runtime implementation
or dependency changes.

## Scope

- WebAssembly as replacement for the Rust core.
- WebAssembly as sandboxed plugin/evaluator ABI.
- WebAssembly as future optional extension.
- WASI capability model and determinism controls.
- Component Model/WIT as a typed ABI candidate.
- Extism as a pragmatic plugin-framework spike candidate.

## Non-scope

- Implementing Wasmtime or Extism now.
- Public package registry.
- Browser runtime support.
- Full hostile-code security audit.
- Finalizing a WIT interface.

## Topic registry link

N/A.

## Source preferences

Prefer official docs and current repository artifacts. Provider output is used
only as critique or synthesis input.

## External source requirement

Required. WASM architecture claims need official Wasmtime, WASI, Component Model,
and plugin framework sources.

## Freshness requirements

Use current source state on 2026-06-24. Treat ecosystem maturity claims as
drift-prone.

## Critic / debate requirement

Use rdlab provider router when available and record which routes returned
substantive output.

## Success criteria

- Separate core replacement from plugin sandbox from deferred extension.
- Identify the smallest architecture change that preserves future WASM use.
- Define a minimal experiment and kill criteria.
- Avoid adding a heavy dependency before evidence requires it.

## Constraints

- One public CLI remains `cak`.
- `cak-runtime-core` should remain pure unless a decision packet explicitly
  changes that invariant.
- Custom skill UX must stay simple.
- Authoritative runtime extensions need lifecycle, provenance, fixture, and
  rollback controls.

## Assumptions

- v0 users can create ordinary CAK-compatible skills without writing Rust.
- Authoritative custom evaluators are a later, higher-risk capability.
- WASM's strongest fit is untrusted executable extension containment, not
  ordinary markdown skill packaging.

## Open questions

- Should CAK reserve a `runtime.kind = wasm_component` descriptor now?
- Should a future WASM spike use raw Wasmtime Component Model or Extism first?
- What latency/binary-size budget is acceptable for a CLI-installed governance
  tool?
