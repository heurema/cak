# 08 Experiments

## Minimal experiment: local Codex skill authoring

Status: not run.

### Goal

Prove that a user can create a CAK-compatible skill with ordinary skill-folder
ergonomics while CAK still records lifecycle, provenance, and host install
state.

### Proposed commands

```sh
cak skill init demo-review --host codex
$EDITOR demo-review/SKILL.md demo-review/cak.yaml
cak skill check ./demo-review
cak skill install ./demo-review --host codex --target <temp-codex-skills-dir>
cak skill list --project .
cak doctor
```

### Expected generated folder

```text
demo-review/
  SKILL.md
  cak.yaml
  fixtures/
    allow.request.json
    block.request.json
```

Optional user files should remain ordinary skill resources:

```text
demo-review/
  scripts/
  references/
  assets/
```

### Expected `cak.yaml` shape

```yaml
id: local.demo-review
version: 0.1.0
kind: advisory

host_package:
  format: agent_skill
  entrypoint: SKILL.md

runtime:
  boundary: eval_request_decision
  mode: host_supplied_facts

admission:
  maturity: draft
  required_fixtures:
    - fixtures/allow.request.json
    - fixtures/block.request.json

trust:
  network_required: false
  side_effect_class: repo_docs_only
```

### Acceptance criteria

- The generated package is a valid ordinary skill folder.
- `cak skill check` rejects missing/invalid `SKILL.md` frontmatter.
- `cak skill check` rejects missing/invalid `cak.yaml` required fields.
- `cak skill install` records id, version, source path, lifecycle maturity,
  provenance refs, and host target.
- Installing into a temp Codex skill directory is repeatable.
- `cak doctor` reports custom skill and adapter compatibility.
- No command calls an LLM or treats `SKILL.md` as runtime policy.

### Kill criteria

- The design requires users to write Rust for ordinary custom skills.
- Any valid `SKILL.md` is treated as admitted without CAK metadata.
- Host install can bypass CAK registry/lock state.
- Update changes a stable/protected skill without a rollback checkpoint.
- The CLI needs a public registry or package manager before local testing.
