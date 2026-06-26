# Adversarial Review - CAK WASM Runtime Architecture

## Attack: WASM adds security theater

WASM is only as safe as the host imports and runtime configuration. If CAK gives
plugins broad WASI, filesystem, network, clock, environment, or logging access,
the sandbox claim becomes weak.

Response:

- no default WASI;
- explicit imports only;
- deterministic fuel;
- memory limits;
- terminal output filtering/capture;
- fixture replay and hostile plugin tests before admission.

## Attack: this is premature ABI lock-in

CAK has not yet proven which user-authored artifacts need runtime authority.
Freezing WIT or Component Model worlds now could constrain the future skill
model.

Response:

- do not freeze WIT now;
- if spiking, use JSON-string ABI over the existing contract first;
- promote to WIT only after fixtures prove a stable evaluator interface.

## Attack: ordinary users will not compile WASM

The user wanted custom skills to be as simple as ordinary skills. WASM toolchain
setup undermines that.

Response:

- ordinary skills remain `SKILL.md` + `cak.yaml`;
- WASM is only for promoted executable evaluators;
- `cak skill build` can later wrap toolchains if the spike proves value.

## Attack: native Rust is enough

Built-in CAK gates can remain Rust crates and tests. No evidence yet proves
polyglot plugins are needed.

Response:

- keep native Rust for built-ins;
- defer WASM dependency;
- revisit only when custom evaluator demand or untrusted-code containment
  becomes concrete.

## Residual risk

The packet is decision-ready for direction, not implementation-ready. Binary
size, latency, and guest toolchain friction are unmeasured.
