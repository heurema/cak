# Debate - CAK Install / Update UX

Status: structured local debate; not a provider transcript.

## Position A: one public `cak` CLI

Argument:

- Users should install and update one product command.
- Runtime and host adapters are implementation details.
- `cak doctor` can explain the active binary, project pin, and adapter state.
- Rollback can be designed around one manifest.

Best objection:

- CAK must own installer state and adapter installation logic earlier than a
  pure runtime project would otherwise need.

Response:

- The install/update contract is part of the product boundary. Deferring it
  creates hidden drift between adapters and runtime behavior.

Verdict: adopt for v0 direction.

## Position B: expose `cakrt` as the runtime command

Argument:

- A separate runtime command makes the internal architecture visible.
- Host wrappers could call the runtime directly.

Best objection:

- Users now have two public product names without a clear lifecycle boundary.
- Update, rollback, and docs become harder to explain.

Response:

- Keep runtime naming internal to crates and docs. The public command should
  remain `cak`.

Verdict: reject as public UX.

## Position C: package-manager-first release

Argument:

- Homebrew, apt, npm, pip, or Cargo gives users familiar install/update paths.
- Some package managers provide signing or checksum infrastructure.

Best objection:

- This optimizes release channels before the core distribution contract is
  proven.
- Each channel has different update and rollback semantics.

Response:

- Treat package managers as later channels. First prove the local lifecycle:
  install, doctor, adapter install, pin, update, rollback.

Verdict: defer.

## Position D: host-specific packages as primary UX

Argument:

- Each host already has its own package conventions.
- A Codex skill or Claude adapter can be distributed independently.

Best objection:

- Policy/runtime behavior can drift across hosts.
- The same project can get different CAK decisions depending on which adapter
  is installed.

Response:

- Host packages can exist as adapter artifacts, but `cak host install <host>`
  should be the primary user action.

Verdict: reject as primary v0 path.

## Position E: background auto-update

Argument:

- Users do not have to think about updates.

Best objection:

- CAK influences policy and governance decisions. Silent changes are unsafe.

Response:

- Keep update explicit and auditable. Revisit only after pins, changelogs,
  signatures, and rollback are proven.

Verdict: reject for v0.
