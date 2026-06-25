# 10 Final Memo

## Executive summary

Recommended v0: support user-created CAK-compatible skills as ordinary skill
folders with a small CAK sidecar descriptor.

```text
SKILL.md      -> host-facing package
cak.yaml      -> CAK-facing lifecycle/provenance/admission metadata
fixtures/     -> executable admission examples
```

The CLI should expose:

```sh
cak skill init <name> --host codex
cak skill check <path>
cak skill install <path> --host codex
cak skill list
```

`cak skill install` should validate and record the package before copying or
linking it into a host skill directory. CAK must not become an LLM runner and
must not execute arbitrary custom runtime logic in v0.

## Decision context

The previous install/update packet chose one public CLI, `cak`. Custom skill
authoring should therefore be part of `cak skill ...`, with host adapters
remaining thin.

## What is known

- Current runtime boundary is pure `EvalRequest -> Decision`.
- Existing CAK skill packaging already demonstrates `SKILL.md` plus `cak.yaml`.
- The skill graph has lifecycle, health, rollback, quarantine, and provenance
  fields.
- The normal skill authoring model is folder-based and should remain familiar.

## What is uncertain

- Registry/lock file names and exact schema.
- Copy vs symlink behavior during local development.
- Minimum fixtures for maturity promotion.
- Non-Codex host install targets.

## What changed

The lab run found one provider suggestion that would simplify UX by making CAK
run LLM prompts from `SKILL.md`, but that conflicts with the runtime boundary.
The recommendation was narrowed to package authoring/admission instead.

## Taxonomy / landscape map

- Ordinary host skill: `SKILL.md`, optional resources, host-discovered.
- CAK-compatible host skill: ordinary host skill plus `cak.yaml` and fixtures.
- CAK-admitted skill: package recorded in CAK registry/skill graph with
  lifecycle and provenance.
- Programmatic runtime skill: future stricter extension with activation and
  intervention behavior; out of v0.

## Key patterns

- Keep authoring simple: folder + edit markdown + install.
- Keep governance explicit: descriptor + fixtures + registry/lock state.
- Keep runtime stable: no LLM runner and no markdown-driven policy execution.

## Anti-patterns

- Public `cakrt`.
- Auto-admitting all `SKILL.md` folders.
- Host-only installs that bypass CAK state.
- User-authored runtime evaluators in v0.

## Opportunity map

- Fast local skill creation for users.
- Clear future path to package registries.
- Consistent install/update/rollback state.
- Better skill lifecycle visibility than raw host folders.

## Risk map

- Too much metadata makes the UX feel unlike ordinary skills.
- Too little metadata makes lifecycle and rollback impossible.
- Multi-host support may sprawl if Codex is not proven first.
- Security testing is still missing for hostile skill packages.

## Recommended experiments

Run the Codex-only local experiment from `08_experiments.md`. Keep it temp-dir
based and local-only.

## Decisions / implications

Draft decision:

- Adopt dual-layer package shape for v0 custom skill authoring.
- Add `cak skill ...` commands before package-manager or registry work.
- Treat runtime plugin/evaluator extension as explicitly deferred.

## Next research questions

- What exact project registry/lock file should `cak skill install` write?
- What fixture threshold moves a skill from `draft` to `candidate`?
- Which host adapter should be second after Codex?

## Evidence notes

This is an internal-first lab run. Provider passes were attempted, but only Agy
returned substantive text, and its main architecture proposal was rejected as
incompatible with the runtime boundary.

## Decision log entry

```text
Date: 2026-06-24
Project: CAK
Decision: Proposed v0 custom skill authoring contract: ordinary SKILL.md package plus cak.yaml descriptor, fixtures, and cak skill init/check/install/list commands.
Reason: Preserves ordinary skill ergonomics while giving CAK lifecycle, provenance, update, and rollback state.
What this prevents: Public cakrt split, host-only skill drift, auto-admitted markdown packages, and turning CAK into an LLM runner.
Review date: After the Codex-only local experiment passes or fails.
```
