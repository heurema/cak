# Target format: CEL policy set (JSON)

Produce one JSON object:

```json
{
  "policies": [
    {
      "id": "P3_refund_above_200_approval",
      "actions": ["billing.refund_order"],
      "enforcement": "require_approval",
      "expr": "args.amount > 200"
    }
  ]
}
```

- `expr` is a CEL expression over the variable `args` (a map of the call
  arguments). Examples: `args.amount > 10000`, `args.environment ==
  'production'`, presence check `!('reason' in args)`, list membership
  `args.environment in ['staging', 'qa']`, always-fire `true`.
- `actions`: exact action names the policy applies to.
- `enforcement`: one of `block`, `require_approval`, `warn`.
- Use ids P1..P10 matching the brief row numbers (suffix free-form).
