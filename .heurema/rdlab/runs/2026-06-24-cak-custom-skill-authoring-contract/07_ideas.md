# 07 Ideas

## Candidate UX

```sh
cak skill init demo-review --host codex
$EDITOR demo-review/SKILL.md demo-review/cak.yaml
cak skill check ./demo-review
cak skill install ./demo-review --host codex
cak skill list
```

## Generated package

```text
demo-review/
  SKILL.md
  cak.yaml
  fixtures/
    allow.request.json
    block.request.json
```

## Template variants

- `advisory`: normal skill with CAK lifecycle metadata.
- `verifier`: skill that asks the host to gather proof facts before invoking
  `cak eval`.
- `workflow`: skill that maps stage/precondition facts into `EvalRequest`.
- `package`: plain host package visible to CAK registry but not authoritative.

## Later ideas

- `cak skill pack` for shareable archives.
- `cak skill promote <id> --to candidate` after fixtures pass.
- `cak skill quarantine <id> --reason <text>`.
- Host-specific template overlays once Claude/Aider/Vibe package conventions
  are verified.
