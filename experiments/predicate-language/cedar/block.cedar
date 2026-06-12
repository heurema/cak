// Tier store: BLOCK. An Allow decision here means a block-tier policy fired.
permit(
  principal,
  action == Action::"crm.create_invoice",
  resource
) when { context.amount <= 0 };

permit(
  principal,
  action == Action::"billing.refund_order",
  resource
) when { !(context has reason) };

permit(
  principal,
  action == Action::"tickets.close_ticket",
  resource
) when { !(context has resolution_note) };

permit(
  principal,
  action == Action::"tickets.delete_ticket",
  resource
);

permit(
  principal,
  action == Action::"billing.refund_order",
  resource
) when { context.amount > context.order_total };

permit(
  principal,
  action == Action::"deploy.promote_release",
  resource
) when { !(["staging", "qa", "production"].contains(context.environment)) };
