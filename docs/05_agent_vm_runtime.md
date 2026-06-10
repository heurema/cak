# 05 — Agent VM Runtime

## Principle

```text
LLM proposes.
Kernel verifies.
Runtime commits.
```

The LLM should not directly mutate the world, memory, skills, policies, or itself.

For governed tools, the LLM process should not hold direct credentials. CAK can
enforce policy only when calls pass through a credential-owning tool gateway.

## Agent VM instruction sketch

```text
OBSERVE
NORMALIZE_STATE
PROPOSE_ACTION
CHECK_CAPABILITY
CHECK_POLICY
SIMULATE
EXECUTE
VERIFY
WRITE_TRACE
WRITE_MEMORY
PROPOSE_EFFECT
PROPOSE_SKILL
PROPOSE_PATCH
REPLAY
PROMOTE
ROLLBACK
QUARANTINE
AUDIT
```

## Example

```text
0: OBSERVE user_intent
1: PROPOSE_ACTION ArchiveInvoice(id=123)
2: CHECK_CAPABILITY Write[Invoice.status]
3: CHECK_POLICY InvoiceSafety
4: SIMULATE ArchiveInvoice(123)
5: ASK_USER preview
6: COMMIT if approved
7: AUDIT
```

## Runtime components

| Component | Responsibility |
|---|---|
| Proposal gateway | Accept only structured proposals |
| State normalizer | Raw observation → typed state |
| Capability checker | Verify authority |
| Effect checker | Classify consequences |
| Policy engine | allow/warn/block/ask/sandbox |
| Transaction manager | preview/commit/rollback/compensate |
| Tool dispatcher | API/UI/MCP/A2A calls |
| Trace recorder | Event-sourced log |
| Verifier hooks | Pre/post/learning/replay checks |
| Budget manager | Tokens, tool calls, latency, risk |
| Audit logger | Explainability and investigations |

## Transaction model

Agents should work as:

```text
propose → preflight → simulate → preview → approve → commit → verify → compensate/rollback → audit
```

not as unguarded `call_tool()`.

## Enforcement boundary

The minimum enforceable runtime pattern is:

```text
agent runtime
  -> structured proposal
  -> verifier
  -> tool gateway
  -> external system
```

If the agent can call the external system directly, CAK is advisory only. The
first implementation should make this boundary explicit before adding learning
or provider portability.
