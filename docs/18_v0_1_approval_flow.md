# 18 - v0.1 Approval Flow

Date: 2026-06-11

## Why this document exists

docs/07 requires approvals to be typed, scoped, logged, and expiring.
docs/17 positions approval depth against hoop's Slack/Teams flow: hoop
approves an operation in a session; CAK approves a typed call.

## Semantics

| Property | v0.1 behavior |
|---|---|
| Scope | exact call: identity + action + sha256(canonical arguments) |
| Lifetime | single-use token, default TTL 15 minutes |
| Queue | file-based: `approvals/{pending,granted,denied}/<id>.json` |
| Operator surface | `python3 -m cak.approve --store <dir> list / grant / deny` |
| Trace | `approval_requested` and `approval_consumed` events |
| Replay | decision events keep the raw verifier verdict; the approval is a separate evidence event, so decision-fidelity checkpoints are unaffected |

## Flow

```text
agent: tools/call (amount=20000)
  -> verifier: require_approval (policy named in typed denial)
  -> gateway: queue pending request, return denial + approval_request_id
operator: python3 -m cak.approve --store .cak/approvals grant <id> --approver vi
agent: identical retry
  -> gateway: consume token (scope match), record approval_consumed, forward
  -> postconditions checked, outcome traced
```

The retry contract is deliberate: the agent never holds an approval token,
and an approval can never widen to a different call — changing any argument
changes the hash and voids the match.

## Non-goals for v0.1

- chat/webhook delivery (Slack, Teams) — adapter concern, later;
- approval batching and risk-tiered auto-approval (docs/01 P2 #13) — needs
  calibrated risk data first;
- delegated approval authority chains (docs/07 governance roles).

## Approval-fatigue guard

Approval requests dedupe by scope while pending: an agent retrying in a loop
creates one queue entry, not a flood.
