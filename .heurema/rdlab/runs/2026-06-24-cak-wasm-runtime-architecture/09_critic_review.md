# 09 Critic Review

## Critical issues

- "WASM is sandboxed" is not enough. CAK still has to configure imports,
  deterministic interruption, memory limits, and capability surfaces.
- "WASM is portable" does not mean it should replace a working pure Rust core.
- Component Model/WIT can create premature ABI lock-in before CAK knows the
  final custom evaluator interface.

## Medium issues

- Wasmtime/Extism dependency size could harm the small CLI install/update
  story.
- WASM skill authoring may be less simple than ordinary skill folders.
- Extism may be easier for a spike but less standards-native than Component
  Model/WIT.
- Native Rust evaluators may be enough until there are real polyglot extension
  users.

## Missing primary sources

- Exact Wasmtime binary size impact in this repo.
- Real multi-language guest build attempts.
- Host-specific needs from Claude/Aider/Vibe adapters.
- Security review of hostile WASM modules under the proposed host imports.

## Unsupported claims

- WASM would make CAK secure by itself.
- WASM would make user skill authoring simple by itself.
- CAK needs WASM for v0 distribution.
- Component Model should be the first implemented custom evaluator ABI.

## Provider / critic debate

| Reviewer | Provider / role | Main objection | Change made or reason rejected |
|---|---|---|---|
| router doctor | local lab probe | Claude, Vibe, and Agy routes available. | Recorded route availability. |
| Agy | synthesis | Reject core replacement; use WASM as plugin ABI later; keep JSON boundary now. | Adopted as main direction. |
| Claude-haiku | critic | Do not choose WASM before skill semantics are proven; risk ABI lock-in. | Adopted as gating condition. |
| Vibe | critic | Returned stop event without content. | Not used. |
| local critic | architecture | Current pure core is the product invariant; WASM belongs outside it. | Adopted. |

## Final confidence rating

High confidence that WASM should not replace the Rust core now.

Medium confidence that WASM should be reserved as a future sandboxed evaluator
ABI.

Low confidence on exact Wasmtime vs Extism implementation choice until a spike
measures DX, binary size, latency, and deterministic replay.
