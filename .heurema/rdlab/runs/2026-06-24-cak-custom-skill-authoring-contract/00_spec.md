# 00 Spec

## Topic

cak custom skill authoring contract

## Project context

CAK currently exposes one public CLI, `cak`, over a Rust runtime boundary:
`EvalRequest` JSON -> `Decision` JSON. The runtime is host-neutral, pure, and
does not parse markdown, call LLMs, inspect repositories, or execute skill
scripts. Host-facing packages are ordinary Agent-Skills-compatible folders with
`SKILL.md`; `skills/cak-rdr-review/cak.yaml` is the current example of an inner
CAK-facing descriptor.

## Decision context

The install/update run chose one public `cak` CLI and rejected public `cakrt`.
This run asks how users can author their own CAK-compatible skills without
writing Rust and without making host adapters drift from the installed CAK
runtime.

## Intended audience

CAK maintainers and early users who want to create local skills that work in
Codex-style hosts while remaining visible to CAK lifecycle, provenance, update,
and rollback checks.

## Output type

Draft architecture proposal and minimal experiment plan. Not a final RDR and
not implementation-ready.

## Scope

- User-created local skill packages.
- Ordinary `SKILL.md` authoring UX.
- Optional CAK descriptor and fixtures.
- Local validation, admission, host install, update, and rollback metadata.
- Codex host first; Claude/Aider/Vibe as later host targets.

## Non-scope

- Public package registry.
- Background auto-update.
- Arbitrary user-authored Rust evaluators.
- Turning CAK into an LLM runner.
- Executing untrusted skill scripts during admission.
- Solving all host-specific package conventions in v0.

## Topic registry link

N/A.

## Source preferences

Use current repository docs and skill artifacts first. External provider output
may be used as critique or idea input, not as source of truth.

## External source requirement

Internal-first run. The immediate question is a CAK product contract against the
existing runtime boundary. External source gathering can be added before a
decision-grade RDR, especially for skill supply-chain security and package
authoring conventions.

## Freshness requirements

Use current repo state on 2026-06-24.

## Critic / debate requirement

Use project `providers.toml` router when available. Record route availability,
successful provider output, failed provider output, and local critique in
`09_critic_review.md`.

## Success criteria

- A user can create a CAK-compatible skill with the same basic mental model as
  ordinary skills: make a folder, edit `SKILL.md`, install it.
- CAK can validate the package shape and record lifecycle/provenance metadata.
- Host adapters remain thin and call `cak`; they do not implement policy.
- The v0 design does not violate the runtime boundary.
- The minimal experiment is small enough to implement before package-manager
  release work.

## Constraints

- One public CLI: `cak`.
- No public `cakrt`.
- Runtime core remains `EvalRequest -> Decision`.
- Users should not need Rust for normal skill authoring.
- Project pins/update/rollback must stay possible.
- Stable/protected skill updates need rollback checkpoints.

## Assumptions

- v0 user-created skills are local and explicitly installed by the user.
- Custom skills can be host-facing packages before they become runtime-control
  skills.
- Programmatic runtime evaluator extensions are a later, stricter contract.

## Open questions

- Should project admission write `.cak/skill-graph.toml`, `.cak/skills.lock`,
  or both?
- Should `cak skill install` copy skill folders or symlink them in developer
  mode?
- What is the minimum fixture set before a user skill can move from `draft` to
  `candidate`?
