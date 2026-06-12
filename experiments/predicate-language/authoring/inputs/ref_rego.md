# Target format: Rego module (OPA 1.x syntax)

Produce one Rego module. Input shape: `input.action` (string),
`input.args` (object). Each rule contributes one fired-policy object:

```rego
package cak

fired contains {"id": "P3_refund_above_200_approval", "enf": "require_approval"} if {
	input.action == "billing.refund_order"
	input.args.amount > 200
}
```

- `enf`: one of `block`, `require_approval`, `warn`.
- Absence check: `not input.args.reason`. Membership:
  `input.args.environment in {"staging", "qa"}`; negated:
  `not input.args.environment in {"staging", "qa"}`.
- Multi-action scope: `input.action in {"a", "b"}`.
- Always-fire for an action: condition on the action only.
- Use ids P1..P10 matching the brief row numbers (suffix free-form).
- The package must be `cak` and the set must be named `fired`.
