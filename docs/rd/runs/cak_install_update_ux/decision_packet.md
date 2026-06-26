# Decision Packet - CAK Install / Update UX

Status: decision-ready for v0 direction; not implementation-ready.

## Decision

Adopt a single public CLI install/update contract for v0:

```text
cak is the product CLI.
Runtime and host adapters are internal subsystems managed by cak.
```

The user-facing model should be:

```sh
cak doctor
cak host list
cak host install codex
cak host install claude
cak update
cak rollback
cak project pin
```

## What this decides

- The public binary name is `cak`.
- Users install one product CLI, not a separate runtime command.
- Host adapters are installed through `cak host install <host>`.
- Python or shell host wrappers are thin launchers over `cak`.
- Updates are explicit, not background.
- Rollback is a first-class v0 requirement.
- Project pins are required before update UX can be called safe for teams.

## What this rejects

- `cakrt` as a public command name.
- Independent host-specific products as the primary install path.
- Auto-update daemon behavior in v0.
- Package-manager-first release as the first implementation step.
- Silent policy/runtime updates in project directories.

## Recommended v0 state files

Global install manifest:

```text
~/.cak/install.toml
```

Suggested fields:

```toml
active_version = "0.1.0"
active_binary = "~/.cak/bin/cak"
previous_version = "0.1.0-pre"

[[host_adapters]]
host = "codex"
version = "0.1.0"
path = "~/.codex/skills/cak-host-adapter"
installed_by = "cak"
```

Project pin:

```text
.cak/cak.toml
```

Suggested fields:

```toml
[runtime]
version = "0.1.0"
policy = "fail_closed_on_mismatch"

[adapters]
codex = "0.1.0"
```

## Quality gate

Decision-ready for v0 direction: pass.

Reasons:

- at least three credible sources were inspected;
- the source ledger is separated from derived pattern and claim matrices;
- internal CAK docs require signed releases, rollback, and versioned audit;
- rustup supports project-pinned toolchain files and explicit precedence;
- uv supports standalone installer and version-specific install URLs;
- GitHub CLI docs show signed package repository and package-manager upgrade
  patterns;
- adversarial review lists supply-chain, drift, and rollback failure modes;
- debate records why package-manager-first, public `cakrt`, and auto-update
  were rejected for v0;
- minimal experiment is specified with acceptance and kill criteria.

Implementation-ready: fail.

Blockers:

- no installer has been written;
- no temp-home install/update/rollback smoke has run;
- no project pin semantics have been tested;
- no host adapter install target has been tested outside the repo checkout;
- no checksum/signature decision exists for public release artifacts.

## Next implementation step

Build the smallest local-only installer experiment:

1. Build `cak` release artifact A and B locally.
2. Add `cak doctor`.
3. Add `cak host install codex --target <path>`.
4. Add `cak project pin`.
5. Add `cak update --from <local-artifact>`.
6. Add `cak rollback`.
7. Run `minimal_experiment.md` end to end.

Do not add Homebrew, npm, pip, package-manager repos, or background updates
until the local experiment passes.
