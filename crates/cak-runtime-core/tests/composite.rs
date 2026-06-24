//! Composite decision-priority and tie-break coverage.

use cak_runtime_core::decision::{DecisionKind, Severity};
use cak_runtime_core::{evaluate, EvalRequest};
use serde_json::json;

fn request(value: serde_json::Value) -> EvalRequest {
    serde_json::from_value(value).expect("valid request")
}

#[test]
fn decision_priority_ordering_is_total() {
    use DecisionKind::{Allow, Ask, Block, InjectContext, Modify, VerifyOnly};
    assert!(Block.priority() > Ask.priority());
    assert!(Ask.priority() > Modify.priority());
    assert!(Modify.priority() > InjectContext.priority());
    assert!(InjectContext.priority() > VerifyOnly.priority());
    assert!(VerifyOnly.priority() > Allow.priority());
}

#[test]
fn severity_priority_ordering_is_total() {
    assert!(Severity::Hard.priority() > Severity::Soft.priority());
    assert!(Severity::Soft.priority() > Severity::Info.priority());
}

#[test]
fn block_short_circuits_to_earliest_evaluator() {
    // `mark_ready` triggers BOTH the stage gate (SG1 mismatch -> block) and the
    // rdr gate (RR1 not-decision-ready -> block). The stage gate runs earlier,
    // so it must win the tie.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "state": { "decision_packet_status": "exploratory" },
        "proposed_action": { "kind": "mark_ready" },
        "skill": { "id": "cak.rdr-review" },
        "stage": { "stage_status": "mismatch", "current_stage": "a", "expected_stage": "b" }
    }));
    let d = evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.severity, Severity::Hard);
    assert_eq!(d.selected_evaluator.as_deref(), Some("stage_gate"));
    assert_eq!(d.violations[0].id, "SG1");
}

#[test]
fn higher_priority_decision_wins_across_evaluators() {
    // `claim_supported` with overclaiming text + open obligations triggers the
    // proof gate (PG3 -> verify_only/soft) AND the rdr gate (RR2 -> modify/soft).
    // `modify` outranks `verify_only`, so the rdr decision wins even though the
    // proof gate runs earlier.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "state": { "c10_status": "hypothesis_level" },
        "proposed_action": {
            "kind": "claim_supported",
            "text": "C10 is a supported architecture decision."
        },
        "skill": { "id": "cak.rdr-review" },
        "proof": {
            "verifier_status": "not_run",
            "grounding_status": "unknown",
            "proof_obligations": ["o1"]
        }
    }));
    let d = evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Modify);
    assert_eq!(d.severity, Severity::Soft);
    assert_eq!(d.selected_evaluator.as_deref(), Some("rdr_review"));
    assert_eq!(d.violations[0].id, "RR2");
}

#[test]
fn all_allow_yields_composite_allow() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "edit_docs" },
        "proposed_action": { "kind": "edit_file", "text": "fix a typo" },
        "skill": { "id": "cak.docs-helper" }
    }));
    let d = evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Allow);
    assert_eq!(d.severity, Severity::Info);
    assert_eq!(d.selected_evaluator, None);
    assert!(d.violations.is_empty());
    assert_eq!(
        d.trace.as_ref().map(|t| t.event.as_str()),
        Some("composite.allow")
    );
}
