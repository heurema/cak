# Target format: Cedar policy stores (three files)

Cedar has no enforcement tiers, so the rules are encoded as three separate
policy stores; an Allow decision in a store means that tier fired. Produce
THREE Cedar policy files in one response, separated by exact marker lines:

```text
// FILE: block.cedar
<policies for every block-tier rule>
// FILE: require_approval.cedar
<policies for every require_approval-tier rule>
// FILE: warn.cedar
<policies for every warn-tier rule>
```

Policy syntax (call arguments arrive as `context`):

```cedar
permit(
  principal,
  action == Action::"billing.refund_order",
  resource
) when { context.amount > 200 };
```

- Multi-action scope: `action in [Action::"a", Action::"b"]`.
- Presence: `context has reason`; absence: `!(context has reason)`.
- Membership: `["staging", "qa"].contains(context.environment)`.
- Always-fire: omit the `when` clause.
- A store may be empty only if no rule belongs to that tier.
