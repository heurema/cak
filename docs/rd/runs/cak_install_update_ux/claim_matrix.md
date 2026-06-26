# Claim Matrix - CAK Install / Update UX

Status: decision support for v0 direction only.

| Claim | Evidence | Confidence | Decision impact | Remaining risk |
|---|---|---:|---|---|
| The public command should remain `cak`, not `cakrt`. | `src_cak_runtime_v0` shows CAK already exposes host-neutral runtime behavior through one CLI; the branch also renamed the public binary to `cak`. | High | Adopt one product CLI. Keep runtime naming internal. | Users may still need docs that distinguish product CLI from internal runtime crates. |
| Host adapters should be installed by `cak`, not as independent products. | `src_cak_runtime_v0` documents the host adapter as a thin launcher over the Rust CLI. | Medium | Add `cak host install <host>` as the user-facing adapter path. | Non-Codex host directories are not yet proven. |
| Project pins are required before update UX is safe for teams. | `src_rustup_overrides` proves checked-in toolchain pins are a mature drift-control pattern; `src_cak_failure_modes` requires auditable runtime/policy changes. | High | Add `.cak/cak.toml` or equivalent before promoting update flows. | Pin semantics are not implemented or tested. |
| Explicit update is safer than background auto-update for v0. | `src_cak_failure_modes` emphasizes rollback and auditability; package-manager examples use explicit upgrade commands. | High | Reject auto-update daemon in v0. | Manual updates are less convenient. |
| Standalone installer is the right first experiment. | `src_uv_installation` and `src_rustup_installation` show standalone CLI install patterns; package-manager docs show extra channel overhead. | Medium | Build a local installer smoke before package-manager publication. | Shell installers require checksum/signature decisions before public release. |
| Rollback must cover more than the binary. | `src_cak_failure_modes` requires canary/rollback; host adapter drift is a CAK-specific failure mode from this analysis. | Medium | Manifest snapshot must include binary and adapter compatibility state. | The exact rollback data model is untested. |

## Unsupported claims

These claims are intentionally not made by this packet:

- CAK is ready for public package-manager distribution.
- CAK has a secure public installer.
- Host adapters for Claude, Aider, and Vibe are implemented.
- Project pin semantics are already enforced.
- Rollback has been proven end to end.
