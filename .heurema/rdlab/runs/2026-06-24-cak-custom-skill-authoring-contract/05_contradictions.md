# 05 Contradictions

## C1: Ordinary skill ergonomics vs CAK admission

Users should be able to create a skill like a normal folder, but CAK cannot
treat every `SKILL.md` folder as trusted or active.

Resolution: keep `SKILL.md` ordinary and add `cak.yaml` plus `cak skill check`
and `cak skill install` for CAK-visible admission.

## C2: No Rust for users vs no markdown-driven runtime policy

Users should not need Rust, but CAK must not execute arbitrary policy logic
from markdown.

Resolution: v0 custom skills are host-facing packages governed by CAK metadata.
Programmatic runtime extensions are deferred.

## C3: Simple install vs rollback correctness

One command should install a skill, but rollback requires recorded version,
source path, host target, lifecycle, and provenance state.

Resolution: `cak skill install` may be the simple command, but it must write
registry/lock state and expose `cak skill check` separately.

## C4: Provider suggestion vs runtime boundary

Agy suggested using `SKILL.md` as an LLM prompt and having CAK output Decision
JSON. This is simpler, but contradicts `docs/22_cak_runtime_v0.md`.

Resolution: reject `cak run <skill>` as an LLM runner for v0.
