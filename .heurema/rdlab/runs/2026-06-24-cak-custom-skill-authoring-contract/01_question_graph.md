# 01 Question Graph

## Root question

How can users create their own CAK-compatible skills with ordinary skill-folder
ergonomics while CAK still preserves lifecycle, provenance, update, and
rollback control?

## Decision questions

- Should v0 custom skills be ordinary host packages, runtime plugins, or both?
- What file makes a normal `SKILL.md` package visible to CAK?
- What command sequence is simple enough for users?
- What should CAK validate before installing a custom skill into a host?
- What state must be recorded for update and rollback?

## Current answers

- v0 should support host-facing packages plus a CAK sidecar descriptor.
- The sidecar should be `cak.yaml`.
- The basic commands should be `cak skill init`, `cak skill check`,
  `cak skill install`, and `cak skill list`.
- Validation should cover `SKILL.md`, `cak.yaml`, fixtures, lifecycle, and
  provenance metadata.
- Runtime plugin/evaluator extensions should be deferred.

## Blockers before implementation-ready

- Registry/lock schema.
- Copy vs symlink decision.
- Fixture minimum for maturity changes.
- Codex temp-dir install smoke.
