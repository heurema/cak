// Tier store: WARN.
permit(
  principal,
  action == Action::"secrets.rotate_key",
  resource
);
