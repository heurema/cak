# CAK Skill Authoring v0

Status: first CLI slice. Package authoring only; not authoritative runtime
plugin execution.

## Decision

User-created CAK-compatible skills start as ordinary host skill folders:

```text
my-skill/
  SKILL.md
  cak.yaml
  fixtures/
    allow.request.json
    block.request.json
```

`SKILL.md` remains the host-facing package. `cak.yaml` is the CAK-facing
descriptor for lifecycle, provenance, fixture, install, and rollback metadata.

## CLI surface

```sh
cak skill init demo-review --host codex --output .
cak skill check ./demo-review
cak skill install ./demo-review --host codex --target <codex-skills-dir>
```

v0 supports Codex host package installation into an explicit `--target`
directory. It intentionally does not write to a live user skill directory unless
the caller passes that directory as the target.

## What `check` validates

- package path is a directory;
- `SKILL.md` exists and has `name` and `description` frontmatter;
- `cak.yaml` exists and has the required v0 keys;
- request fixtures under `fixtures/*.request.json` parse as `EvalRequest`.

The check is shape validation, not semantic proof that a skill is useful or
safe.

## What `install` records

`cak skill install` validates the package, copies it into the target host skill
directory, and writes:

```text
.cak-install.json
```

The metadata records `installed_by`, `host`, `skill_id`, `version`, `kind`,
`source_path`, `install_path`, and install time.

## Runtime boundary

This feature does not change `cak-runtime-core`.

The Rust core remains the authoritative pure runtime:

```text
EvalRequest -> Decision
```

Ordinary custom skills do not require Rust or WASM. Future authoritative
executable evaluators may use a separate WASM runner, but that is explicitly
deferred to a later spike.

## Related research packets

- `docs/rd/runs/cak_install_update_ux/`
- `docs/rd/runs/cak_wasm_runtime_architecture/`
