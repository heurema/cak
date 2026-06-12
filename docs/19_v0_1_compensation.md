# 19 - v0.1 Compensation

Date: 2026-06-12

## Why this document exists

`Effect<compensable>` is only honest if the system knows *how* to compensate
and can prove the compensation happened. docs/05 names the transaction model
(`... -> compensate/rollback -> audit`); docs/17 lists typed effects and the
saga chain as capabilities no shipping gateway has.

## CompensationSpec

A compensable effect declares its undo as a typed reference to another
governed action, with derived — not free-typed — arguments:

```json
{
  "id": "effect.crm.create_invoice",
  "reversibility": "compensable",
  "compensation": {
    "action": "crm.void_invoice",
    "args_from_result": { "invoice_id": "invoice.id" }
  }
}
```

`args_from_result` paths resolve against the recorded tool result;
`args_from_args` against the original call arguments. If any path fails to
resolve, no compensation is prepared — absence is recorded, not guessed.

## Trace events

| Event | When |
|---|---|
| `compensation_prepared` | A compensable effect completed and all argument paths resolved; carries the ready-to-fire call (action + derived arguments) |
| `compensation_suggested` | A postcondition evaluated FALSE after execution; references the prepared call when one exists |
| `compensation_executed` | The prepared call was issued, passed the verifier, and completed without error; carries `compensates_call_id`, closing the saga chain |

## Rules

- **Nothing auto-fires.** The gateway prepares and suggests; the agent or the
  operator decides. Auto-compensation is a policy decision deferred until
  risk data exists (same posture as approval batching, docs/18).
- **No bypass.** A compensation call is an ordinary governed action: it needs
  a capability, an ActionSpec, and passes policies — `crm.void_invoice` being
  a compensation does not exempt it from the verifier.
- **Exact linkage.** The executed call is matched to the prepared one by
  action + sha256 of derived arguments (the approval-scope mechanism reused),
  so the audit chain cannot be claimed by a different call.

## Non-goals for v0.1

- multi-step sagas and ordering guarantees;
- auto-fire policies and retry semantics;
- distributed/cross-system transactions;
- compensation of `irreversible` effects (by definition; the verifier treats
  them as approval/block territory instead).
