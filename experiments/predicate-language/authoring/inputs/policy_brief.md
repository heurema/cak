# Policy brief: gateway rules for an operations agent

Write the following 10 rules as machine-evaluable policies. Enforcement
tiers, strictest wins: `block` > `require_approval` > `warn` > allow
(no rule fired).

| # | Applies to action(s) | Rule | Tier |
|---|---|---|---|
| 1 | crm.create_invoice, crm.send_invoice | amount greater than 10000 | require_approval |
| 2 | crm.create_invoice | amount is zero or negative | block |
| 3 | billing.refund_order | amount greater than 200 | require_approval |
| 4 | deploy.promote_release | environment equals "production" | require_approval |
| 5 | secrets.rotate_key | always (every call) | warn |
| 6 | billing.refund_order | the "reason" argument is absent | block |
| 7 | tickets.close_ticket | the "resolution_note" argument is absent | block |
| 8 | tickets.delete_ticket | always (every call) | block |
| 9 | billing.refund_order | amount greater than the order_total argument | block |
| 10 | deploy.promote_release | environment is NOT one of: staging, qa, production | block |

Call arguments are flat JSON objects (numbers, strings). A rule must fire
only for its listed action(s).
