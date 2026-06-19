# 20 - v0.1 CEL Policy Predicates

Date: 2026-06-15

## Why this document exists

docs/11 ratified CEL (Common Expression Language) for `PolicySpec`
predicates, based on exp-005 (lab): CEL, Rego, and Cedar all covered the
policy corpus and passed two-vendor cold-draft authoring, but CEL is the only
in-process Python option and stays far below the verifier latency budget
(p99 ~0.4 ms vs the 500 ms gateway budget).

## What changed

`PolicySpec` gains an optional `expr` field — a single CEL boolean
expression over `args` (the call arguments):

```json
{
  "id": "policy.refund_exceeds_order_total",
  "name": "refund_exceeds_order_total",
  "actions": ["billing.refund_order"],
  "enforcement": "block",
  "expr": "args.amount > args.order_total"
}
```

This expresses what the interim surface (docs/14, predicates.py) cannot:
cross-field comparison, list membership (`args.environment in ['staging',
'qa']`), and field absence (`!('reason' in args)`).

## What CAK keeps (not a framework, a language)

The verdict was deliberate: CAK adopts a predicate *language*, not a policy
*framework*. The `PolicySpec` envelope stays CAK-owned:

- action scope (`actions`);
- enforcement tiers (`allow | warn | block | require_approval`);
- strictest-wins resolution across fired policies.

CEL only answers "did this one policy's condition hold?".

## Migration and compatibility

- A policy carries **either** `expr` (CEL) **or** `when` (interim list),
  never both — load fails otherwise.
- The interim `when` surface is deprecated but still evaluated, so existing
  configs run unchanged. Empty `when` with no `expr` still fires
  unconditionally (the exp-004 finding).
- `cel-python` is a declared dependency but optional at runtime: configs
  using only `when` run without it. A config declaring `expr` while celpy is
  absent fails at load with a clear message, never silently.

## Semantics

- `expr` is compiled and validated at config-load time (invalid syntax →
  `ConfigError`).
- An expression that cannot be evaluated against the given arguments
  (missing field, type error) does **not** fire the policy — unevaluable is
  never a guess (docs/14), matching the interim surface.

## Out of scope for v0.1

- migrating effect pre/postconditions (`preconditions`, `causes`) off the
  interim surface — policies first;
- Rego/Cedar export (docs/11: Rego as an OPA translation target, Cedar as a
  future verification-export target).
