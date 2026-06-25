# Hypothesis Matrix - CAK Install / Update UX

Status: v0 direction selected; implementation not started.

| Hypothesis | Description | Supports | Weaknesses | Minimal experiment | Verdict |
|---|---|---|---|---|---|
| H1: one public `cak` installer plus host adapters | User installs one `cak` binary. Host wrappers are installed and updated through `cak host install <host>`. | One product name, one runtime version source, easier doctor/update/rollback, adapters stay thin. | Requires CAK to own installer state and adapter copy/update logic. | Install into temp home, run `cak doctor`, install Codex adapter, update, rollback, rerun fixture. | Adopt for v0. |
| H2: host-specific packages only | Each host gets its own skill/plugin package and installer path. | Simple per-host start; matches host package conventions. | Runtime version drift, duplicate update UX, harder rollback, more docs. | Install Codex and Claude adapters independently and compare runtime version behavior. | Reject as primary v0 path; keep adapters as outputs of `cak host install`. |
| H3: package-manager-first distribution | Publish through Homebrew, Cargo, pip, npm, or OS package repos first. | Familiar update commands when mature; signed package repos possible. | Release overhead before contract stabilizes; each ecosystem has separate policy. | Publish internal formula/package and test update. | Defer. Useful after standalone installer stabilizes. |
| H4: cargo install only | Users run `cargo install --path` or install from a crate. | Easy for Rust developers. | Not enough for non-Rust users; does not install host adapters; rollback and pins are weak. | Install in a temp Cargo home and run host adapter setup separately. | Use only as developer fallback, not product UX. |
| H5: auto-update daemon | CAK updates itself in the background. | Low user friction. | Dangerous for policy/runtime behavior; hard to audit and roll back; violates predictable governance. | Not needed. | Reject for v0. |

## Selected v0 shape

Use H1:

```text
cak install/update state
  owns one public binary: cak
  owns host adapter install/update
  supports project pin
  supports explicit update
  supports rollback
```

H2 remains useful as packaging detail: host adapters can still be skill folders
or plugin bundles, but users should not install them as independent products.

H3 is a later release-channel layer. Package-manager installs should delegate
updates to the package manager once CAK publishes through those channels.

## Command surface candidate

```sh
cak doctor
cak host list
cak host install codex
cak host install claude
cak update
cak rollback
cak project pin
```

## Precedence candidate

The v0 precedence should be intentionally small:

1. Explicit CLI flag, for example `--cak-version` or `--binary`.
2. Project pin, for example `.cak/cak.toml`.
3. Global install state, for example `~/.cak/install.toml`.
4. PATH fallback for development.

Avoid adding environment-variable precedence in v0 unless CI proves it is
needed.
