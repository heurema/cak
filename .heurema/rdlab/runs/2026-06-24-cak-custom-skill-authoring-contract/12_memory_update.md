# 12 Memory Update

No long-term memory update requested by the user.

Candidate memory only if explicitly requested later:

- CAK custom skill authoring v0 should preserve ordinary `SKILL.md` folder UX
  while adding a `cak.yaml` sidecar, fixtures, and `cak skill init/check/install`
  commands.
- Reject `cak run <skill>` as an LLM runner because it violates the current
  `EvalRequest -> Decision` runtime boundary.
