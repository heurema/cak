# 06 Synthesis

## What is known

- CAK's runtime boundary is `EvalRequest` JSON -> `Decision` JSON.
- Host-facing packages can use ordinary `SKILL.md`; CAK-facing metadata can sit
  beside it in `cak.yaml`.
- The existing skill graph already has lifecycle and provenance fields.
- Users need a simple authoring path that does not require Rust.

## What is uncertain

- The exact project registry file name and lock format.
- Whether v0 should copy or symlink installed local skills.
- Which host package targets beyond Codex should be included in the first
  experiment.
- The minimum fixture set required for promotion beyond `draft`.

## What changed recently

The public command decision moved from a possible split CLI to one public
`cak` command. Custom skill authoring should therefore be exposed as
`cak skill ...`, not as a separate runtime tool.

## Patterns

- Dual-layer package:
  - outer host package: `SKILL.md`, optional `scripts/`, `references/`,
    `assets/`;
  - inner CAK descriptor: `cak.yaml`;
  - optional fixtures under `fixtures/`.
- Simple path:
  - `cak skill init <name>`;
  - edit `SKILL.md` and `cak.yaml`;
  - `cak skill check ./<name>`;
  - `cak skill install ./<name> --host codex`.
- Install performs local admission:
  - validate shape;
  - run fixture checks when present;
  - record lifecycle/provenance metadata;
  - copy or link into host skill directory;
  - update CAK registry/lock state.

## Anti-patterns

- `cak run <skill>` as an LLM runner over `SKILL.md`. This violates the current
  runtime boundary.
- Treating any `SKILL.md` folder as automatically trusted or active.
- Letting host-specific package installs bypass CAK registry/lifecycle state.
- Requiring users to write Rust for ordinary local skills.
- Letting custom skills add arbitrary executable policy to CAK core in v0.

## Open problems

- Registry naming:
  - global: `~/.cak/skills/registry.toml` or included in `~/.cak/install.toml`;
  - project: `.cak/skills.lock` or `.cak/skill-graph.toml`.
- Fixture minimum:
  - at least one allow/control request;
  - at least one blocked or modified decision if the skill claims authority;
  - rollback checkpoint for stable/protected updates.
- Host target behavior:
  - Codex first because the repo already has Agent-Skills-compatible packages;
  - Claude/Aider/Vibe after their install directories and metadata conventions
    are confirmed.

## Strategic implications

The smallest viable product is not a generic skill runtime. It is a package
authoring and admission contract that keeps ordinary skill ergonomics while
preserving CAK governance.

## Opportunity map

- Users get a familiar folder-based authoring path.
- CAK gets explicit metadata for lifecycle, provenance, update, and rollback.
- Host adapters remain thin and auditable.
- Future package registries can build on the same descriptor and lock state.

## Risk map

- A too-simple install path could admit unsafe skill packages.
- Too much required metadata would make custom skills feel unlike normal
  skills.
- Copying skills into host directories can create drift unless CAK records the
  installed version and source path.
- Symlinks are convenient for local development but may be brittle across hosts.

## Recommended experiments

Build one Codex-only local experiment:

1. `cak skill init demo-review --host codex`.
2. Edit the generated `SKILL.md` and `cak.yaml`.
3. Add two fixture requests.
4. Run `cak skill check ./demo-review`.
5. Run `cak skill install ./demo-review --host codex --target <temp-dir>`.
6. Verify registry/lock state records id, version, source path, lifecycle,
   provenance refs, and installed host target.
7. Run `cak host install codex` and verify the host adapter sees the admitted
   skill graph.
8. Update the skill version and require a rollback checkpoint before promoting
   stable/protected maturity.
