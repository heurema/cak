# 09 Critic Review

## Critical issues

- Do not let "custom CAK skill" mean "arbitrary user-authored runtime
  evaluator". That would reopen the runtime DSL/plugin problem and violate the
  v0 non-goals.
- Do not turn CAK into an LLM runner that reads `SKILL.md` as a system prompt.
  Provider output suggested this, but it conflicts with the repo's runtime
  boundary.
- Do not auto-admit local `SKILL.md` folders. Ordinary skills are useful host
  packages, not automatically trusted runtime-control artifacts.

## Medium issues

- The registry/lock file needs a clear split between global install state and
  project-pinned skill graph state.
- Copy vs symlink has real rollback implications.
- `cak skill install` may become too magical if it both admits and installs.
  The v0 CLI should expose `check` separately even if `install` calls it.

## Minor issues

- `kind` values should reuse existing runtime terms where possible:
  `package`, `workflow`, `verifier`, `intervention`, `hybrid`.
- Templates should be intentionally sparse; ordinary skills should not be
  buried under CAK metadata.

## Missing primary sources

- Host-specific skill packaging docs for Claude, Aider, and Vibe.
- Security papers/repos specifically about malicious skill packages should be
  rechecked before a decision-grade RDR.
- Package install conventions for copying vs linking skill folders.

## Unsupported claims

- "CAK can safely execute custom user policy" is unsupported.
- "All host adapters can install custom skills the same way" is unsupported.
- "Project pin semantics are already enough" is unsupported.

## Provider / critic debate

| Reviewer | Provider / role | Main objection | Change made or reason rejected |
|---|---|---|---|
| router doctor | local lab probe | `claude-sonnet`, `claude-haiku`, `vibe-default`, and `agy-default` were available. | Availability recorded, but not treated as synthesis evidence. |
| Claude run | synthesis | Command hung with no stdout until interrupted. | Not used. |
| Vibe run | critic | Returned `<vibe_stop_event>Turn limit of 1 reached</vibe_stop_event>` and no critique. | Not used except as tooling limitation. |
| Agy run | synthesis | Proposed `cak run <name>` that injects `SKILL.md` into an LLM prompt and outputs Decision JSON. | Rejected because CAK v0 is not an LLM runner and does not parse markdown. |
| local critic | architecture | The simplest safe path is ordinary skill package + `cak.yaml` + fixtures + local admission, not runtime plugin execution. | Adopted as draft recommendation. |

## Overconfident recommendations

- Calling this implementation-ready would be overconfident.
- Claiming multi-host support before Codex temp-dir install works would be
  overconfident.
- Claiming secure custom skills before hostile package tests would be
  overconfident.

## Final confidence rating

Medium for v0 direction. Low for implementation details until the Codex-only
local experiment runs.
