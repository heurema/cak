// Tier store: REQUIRE_APPROVAL.
permit(
  principal,
  action in [Action::"crm.create_invoice", Action::"crm.send_invoice"],
  resource
) when { context.amount > 10000 };

permit(
  principal,
  action == Action::"billing.refund_order",
  resource
) when { context.amount > 200 };

permit(
  principal,
  action == Action::"deploy.promote_release",
  resource
) when { context.environment == "production" };
