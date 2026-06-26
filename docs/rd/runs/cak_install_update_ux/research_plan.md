# Research Plan - CAK Install / Update UX

## Research question

How should a user install, update, pin, and roll back CAK in v0 without creating
multiple public command names or host-specific distribution drift?

## Scope

- Local developer installation.
- CI installation.
- Host adapter installation for Codex, Claude, Aider, and Vibe-style hosts.
- Version pinning for project repositories.
- Update and rollback behavior.
- Doctor/smoke checks that prove the installed CLI and adapters are usable.

## Non-goals

- Homebrew, npm, pip, apt, dnf, or winget publishing in the first step.
- Background auto-update daemon.
- Remote policy marketplace.
- Live interception inside every host.
- Hosted CAK service or account system.
- Changing the runtime decision contract.

## Current project facts

- The public command name is now `cak`.
- `crates/cak-runtime-cli` builds the public CLI binary.
- `cak gate --proposal <path>` maps a host proposal into a host-facing outcome.
- `skills/cak-host-adapter` is a thin Python launcher over `cak gate`.
- Runtime v0 is host-neutral: the host gathers facts and encodes request JSON.

## Source strategy

Inspect examples that have similar installation pressure:

- standalone CLI installer with versioned URL;
- project-pinned tool version;
- package-manager upgrade commands;
- signed package repositories or checksum guidance;
- internal CAK rollback and signed-release requirements.

Only inspected sources may support claims in `source_ledger.yaml`. Sources that
failed to load remain leads, not evidence.

## Expected objections

- A shell installer can become supply-chain risk.
- A single global `cak` binary can silently change project behavior.
- Per-host packages may be simpler than one installer.
- Keeping rollback history locally may complicate v0 implementation.
- Host adapters may drift from the installed CLI if they are copied manually.

## Minimal experiment candidates

- Install a local release artifact into a temporary home.
- Run `cak doctor`.
- Install one host adapter into a temporary host directory.
- Pin a project to a specific CAK version.
- Update from version A to version B.
- Roll back from version B to version A.
- Run `cak gate` before and after update/rollback on the same fixture.

## Stop rules

Stop and narrow the design if:

- project pinning cannot prevent silent behavior drift;
- rollback cannot restore both binary and host adapter state;
- install/update needs host-specific logic before the core CLI exists;
- the first installer requires a public package manager release.
