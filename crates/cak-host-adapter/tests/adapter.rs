use cak_host_adapter::{evaluate_proposal, HostOutcomeKind, HostProposal};
use cak_runtime_core::DecisionKind;
use pretty_assertions::assert_eq;
use serde_json::json;

fn proposal(value: serde_json::Value) -> HostProposal {
    serde_json::from_value(value).expect("valid host proposal")
}

#[test]
fn maps_all_decision_kinds_to_host_outcomes() {
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::Allow),
        HostOutcomeKind::Proceed
    );
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::Block),
        HostOutcomeKind::Deny
    );
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::Modify),
        HostOutcomeKind::NeedsModification
    );
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::InjectContext),
        HostOutcomeKind::InjectContext
    );
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::Ask),
        HostOutcomeKind::NeedsConfirmation
    );
    assert_eq!(
        HostOutcomeKind::from_decision(DecisionKind::VerifyOnly),
        HostOutcomeKind::NeedsVerification
    );
}

#[test]
fn maps_allow_to_proceed() {
    let proposal = proposal(json!({
        "schema_version": "0.1.0",
        "host": { "name": "test-host", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "mark_ready" },
        "skill": { "id": "workflow.runner" }
    }));

    let outcome = evaluate_proposal(&proposal);

    assert_eq!(outcome.outcome, HostOutcomeKind::Proceed);
    assert_eq!(
        outcome.decision.decision,
        cak_runtime_core::DecisionKind::Allow
    );
}

#[test]
fn maps_block_to_deny() {
    let proposal = proposal(json!({
        "schema_version": "0.1.0",
        "host": { "name": "test-host", "mode": "ci" },
        "task": { "kind": "review_trace_corpus" },
        "state": { "trace_plan_status": "pending" },
        "proposed_action": { "kind": "accept_trace_corpus" },
        "skill": { "id": "cak.rdr-review" }
    }));

    let outcome = evaluate_proposal(&proposal);

    assert_eq!(outcome.outcome, HostOutcomeKind::Deny);
    assert_eq!(
        outcome.decision.selected_evaluator.as_deref(),
        Some("rdr_review")
    );
}

#[test]
fn maps_ask_to_needs_confirmation() {
    let proposal = proposal(json!({
        "schema_version": "0.1.0",
        "host": { "name": "test-host", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "mark_ready" },
        "skill": { "id": "workflow.runner" },
        "stage": { "stage_status": "preconditions_missing" }
    }));

    let outcome = evaluate_proposal(&proposal);

    assert_eq!(outcome.outcome, HostOutcomeKind::NeedsConfirmation);
    assert_eq!(
        outcome.decision.selected_evaluator.as_deref(),
        Some("stage_gate")
    );
}
