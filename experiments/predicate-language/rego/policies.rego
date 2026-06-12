package cak

# Each rule contributes a fired-policy object; the adapter applies
# strictest-wins, mirroring the cak verifier.

fired contains {"id": "P1_high_amount_approval", "enf": "require_approval"} if {
	input.action in {"crm.create_invoice", "crm.send_invoice"}
	input.args.amount > 10000
}

fired contains {"id": "P2_nonpositive_amount_block", "enf": "block"} if {
	input.action == "crm.create_invoice"
	input.args.amount <= 0
}

fired contains {"id": "P3_refund_above_200_approval", "enf": "require_approval"} if {
	input.action == "billing.refund_order"
	input.args.amount > 200
}

fired contains {"id": "P4_production_promotion_approval", "enf": "require_approval"} if {
	input.action == "deploy.promote_release"
	input.args.environment == "production"
}

fired contains {"id": "P5_rotation_warn", "enf": "warn"} if {
	input.action == "secrets.rotate_key"
}

fired contains {"id": "P6_refund_requires_reason", "enf": "block"} if {
	input.action == "billing.refund_order"
	not input.args.reason
}

fired contains {"id": "P7_close_requires_note", "enf": "block"} if {
	input.action == "tickets.close_ticket"
	not input.args.resolution_note
}

fired contains {"id": "P8_never_delete", "enf": "block"} if {
	input.action == "tickets.delete_ticket"
}

fired contains {"id": "P9_refund_exceeds_order_total", "enf": "block"} if {
	input.action == "billing.refund_order"
	input.args.amount > input.args.order_total
}

fired contains {"id": "P10_unknown_environment_block", "enf": "block"} if {
	input.action == "deploy.promote_release"
	not input.args.environment in {"staging", "qa", "production"}
}
