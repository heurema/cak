# Minimal Experiment - CAK Install / Update UX

Status: not run.

This experiment is the gate from decision-ready to implementation-ready.

## Goal

Prove that one public `cak` installer can manage the binary, host adapters,
project pins, updates, rollbacks, and smoke checks without relying on public
package-manager distribution.

## Fixtures

Use two locally built release candidates:

- `cak` version A;
- `cak` version B.

Use at least one host adapter fixture:

- Codex-style skill folder using `skills/cak-host-adapter`;
- optional Claude/Aider/Vibe placeholders if their host package directories are
  known.

Use one proposal fixture:

```text
runtime-fixtures/rdr-review/pending_trace_status_blocked.request.json
```

## Experiment steps

1. Create an isolated temp home and temp project.
2. Install version A into the temp home.
3. Run `cak doctor`.
4. Run `cak gate --proposal <fixture>` and record the outcome.
5. Run `cak host install codex --target <temp-host-dir>`.
6. Verify the installed host wrapper calls the temp-home `cak`.
7. Run `cak project pin <version-A>` in the temp project.
8. Update to version B.
9. Verify global `cak --version` reports B.
10. Verify the project-pinned invocation still uses A or refuses drift,
    depending on the chosen pin semantics.
11. Run `cak rollback`.
12. Verify global `cak --version` reports A.
13. Verify host adapter state rolled back or remains compatible.
14. Run the same `cak gate` fixture after rollback and compare output.

## Acceptance criteria

- A user can install without Cargo.
- `cak doctor` detects missing binary, PATH issues, missing host adapter, and
  version mismatch.
- Host adapter install is repeatable and idempotent.
- Project pin prevents silent behavior drift.
- Update is explicit.
- Rollback restores the prior binary and compatible adapter state.
- The fixture outcome is stable across install/update/rollback unless the
  version change is intentionally breaking and visible.

## Kill criteria

- Rollback cannot restore a known-good binary.
- Host adapters can silently point at a different binary than the project pin.
- Update changes policy/runtime behavior without surfacing the version change.
- The installer needs public Homebrew/npm/pip infrastructure before it can be
  tested locally.
