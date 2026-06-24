//! Positive and negative rule coverage for each evaluator in isolation.

use cak_runtime_core::decision::{DecisionKind, Severity};
use cak_runtime_core::lifecycle_gate::LifecycleGateEvaluator;
use cak_runtime_core::proof_gate::ProofGateEvaluator;
use cak_runtime_core::rdr_review::RdrReviewEvaluator;
use cak_runtime_core::stage_gate::StageGateEvaluator;
use cak_runtime_core::{Decision, EvalRequest, Evaluator};
use serde_json::json;

fn request(value: serde_json::Value) -> EvalRequest {
    serde_json::from_value(value).expect("valid request")
}

fn assert_allow(decision: &Decision) {
    assert_eq!(decision.decision, DecisionKind::Allow, "expected allow");
    assert_eq!(decision.severity, Severity::Info);
}

fn skill_graph(maturity: &str, rollback: Option<&str>) -> serde_json::Value {
    json!({
        "nodes": [{
            "id": "skill.x",
            "kind": "intervention",
            "version": "1.0.0",
            "lifecycle": {
                "maturity": maturity,
                "health": "unknown",
                "rollback_checkpoint": rollback
            },
            "provenance_refs": ["trace.1"]
        }],
        "edges": []
    })
}

// ----- LifecycleGateEvaluator -----

#[test]
fn lg1_blocks_quarantined_activation() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "activate_skill" },
        "proposed_action": { "kind": "activate_skill", "skill_id": "skill.x" },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("quarantined", None)
    }));
    let d = LifecycleGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.severity, Severity::Hard);
    assert_eq!(d.violations[0].id, "LG1");
}

#[test]
fn lg2_blocks_stable_update_without_rollback() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "update_skill" },
        "proposed_action": { "kind": "update_skill", "skill_id": "skill.x" },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("stable", None)
    }));
    let d = LifecycleGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.violations[0].id, "LG2");
}

#[test]
fn lg2_allows_stable_update_with_rollback() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "update_skill" },
        "proposed_action": { "kind": "update_skill", "skill_id": "skill.x" },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("stable", Some("ckpt.1"))
    }));
    assert_allow(&LifecycleGateEvaluator.evaluate(&req));
}

#[test]
fn lg3_asks_on_draft_authoritative_activation() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "activate_skill" },
        "proposed_action": { "kind": "activate_skill", "skill_id": "skill.x", "authority": "authoritative" },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("draft", None)
    }));
    let d = LifecycleGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Ask);
    assert_eq!(d.severity, Severity::Soft);
    assert_eq!(d.violations[0].id, "LG3");
}

#[test]
fn lifecycle_blocks_quarantined_authority_claim() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "claim_authority" },
        "proposed_action": {
            "kind": "claim_authority",
            "skill_id": "skill.x",
            "authority": "authoritative"
        },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("quarantined", None)
    }));
    let d = LifecycleGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.severity, Severity::Hard);
    assert_eq!(d.violations[0].id, "LG4");
}

#[test]
fn lifecycle_allows_when_no_graph_or_no_match() {
    // No graph at all.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "activate_skill" },
        "proposed_action": { "kind": "activate_skill", "skill_id": "skill.x" },
        "skill": { "id": "loader" }
    }));
    assert_allow(&LifecycleGateEvaluator.evaluate(&req));

    // Graph present but no node matches the target id.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "activate_skill" },
        "proposed_action": { "kind": "activate_skill", "skill_id": "skill.missing" },
        "skill": { "id": "loader" },
        "skill_graph": skill_graph("quarantined", None)
    }));
    assert_allow(&LifecycleGateEvaluator.evaluate(&req));
}

#[test]
fn lifecycle_falls_back_to_skill_ref_id() {
    // No skill_id on the action: target resolves from skill.id.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "plugin" },
        "task": { "kind": "activate_skill" },
        "proposed_action": { "kind": "activate_skill" },
        "skill": { "id": "skill.x" },
        "skill_graph": skill_graph("deprecated", None)
    }));
    let d = LifecycleGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.violations[0].id, "LG1");
}

// ----- StageGateEvaluator -----

#[test]
fn sg1_blocks_on_mismatch() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "complete_workflow" },
        "skill": { "id": "runner" },
        "stage": { "stage_status": "mismatch", "current_stage": "a", "expected_stage": "b" }
    }));
    let d = StageGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.violations[0].id, "SG1");
}

#[test]
fn sg2_asks_on_preconditions_missing() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "execute_stage_bound_action" },
        "skill": { "id": "runner" },
        "stage": { "stage_status": "preconditions_missing" }
    }));
    let d = StageGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Ask);
    assert_eq!(d.violations[0].id, "SG2");
}

#[test]
fn sg2_asks_on_mark_ready_with_preconditions_missing() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "mark_ready" },
        "skill": { "id": "runner" },
        "stage": { "stage_status": "preconditions_missing" }
    }));
    let d = StageGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Ask);
    assert_eq!(d.violations[0].id, "SG2");
}

#[test]
fn stage_allows_without_context_or_on_active() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "complete_workflow" },
        "skill": { "id": "runner" }
    }));
    assert_allow(&StageGateEvaluator.evaluate(&req));

    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "cli" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "complete_workflow" },
        "skill": { "id": "runner" },
        "stage": { "stage_status": "active" }
    }));
    assert_allow(&StageGateEvaluator.evaluate(&req));
}

// ----- ProofGateEvaluator -----

#[test]
fn pg1_blocks_unverified_claim_and_wins_over_grounding() {
    // verifier not passed AND grounding suspect: PG1 block must win.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "accept_claim" },
        "proposed_action": { "kind": "claim_verified" },
        "skill": { "id": "gate" },
        "proof": { "verifier_status": "failed", "grounding_status": "suspect" }
    }));
    let d = ProofGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.severity, Severity::Hard);
    assert_eq!(d.violations[0].id, "PG1");
}

#[test]
fn pg2_verify_only_when_grounding_suspect_but_verifier_passed() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "accept_claim" },
        "proposed_action": { "kind": "mark_verified" },
        "skill": { "id": "gate" },
        "proof": { "verifier_status": "passed", "grounding_status": "unknown" }
    }));
    let d = ProofGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::VerifyOnly);
    assert_eq!(d.violations[0].id, "PG2");
}

#[test]
fn pg3_verify_only_on_text_overclaim() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "post_comment" },
        "proposed_action": { "kind": "post_comment", "text": "This result is fully supported." },
        "skill": { "id": "gate" },
        "proof": { "verifier_status": "not_run", "grounding_status": "unknown", "proof_obligations": ["o1"] }
    }));
    let d = ProofGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::VerifyOnly);
    assert_eq!(d.violations[0].id, "PG3");
}

#[test]
fn proof_blocks_text_overclaim_when_verifier_failed() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "post_comment" },
        "proposed_action": { "kind": "post_comment", "text": "This result is fully supported." },
        "skill": { "id": "gate" },
        "proof": {
            "verifier_status": "failed",
            "grounding_status": "grounded",
            "proof_obligations": ["o1"],
            "counterexample_refs": ["cx.1"]
        }
    }));
    let d = ProofGateEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.severity, Severity::Hard);
    assert_eq!(d.violations[0].id, "PG4");
}

#[test]
fn proof_allows_when_passed_and_grounded() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "accept_claim" },
        "proposed_action": { "kind": "claim_verified" },
        "skill": { "id": "gate" },
        "proof": { "verifier_status": "passed", "grounding_status": "grounded" }
    }));
    assert_allow(&ProofGateEvaluator.evaluate(&req));

    // No proof context: allow.
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "accept_claim" },
        "proposed_action": { "kind": "claim_verified" },
        "skill": { "id": "gate" }
    }));
    assert_allow(&ProofGateEvaluator.evaluate(&req));
}

// ----- RdrReviewEvaluator -----

#[test]
fn rr1_blocks_merge_when_not_decision_ready() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "state": { "decision_packet_status": "exploratory" },
        "proposed_action": { "kind": "recommend_merge" },
        "skill": { "id": "cak.rdr-review" }
    }));
    let d = RdrReviewEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.violations[0].id, "RR1");
}

#[test]
fn rr1_allows_merge_when_decision_ready() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "state": { "decision_packet_status": "decision_ready" },
        "proposed_action": { "kind": "recommend_merge" },
        "skill": { "id": "cak.rdr-review" }
    }));
    assert_allow(&RdrReviewEvaluator.evaluate(&req));
}

#[test]
fn rr1_allows_non_rdr_mark_ready_without_packet_status() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "run_workflow" },
        "proposed_action": { "kind": "mark_ready" },
        "skill": { "id": "workflow.runner" }
    }));
    assert_allow(&RdrReviewEvaluator.evaluate(&req));
}

#[test]
fn rr2_modifies_c10_overclaim() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "state": { "c10_status": "hypothesis_level" },
        "proposed_action": { "kind": "claim_supported", "text": "C10 is a supported decision." },
        "skill": { "id": "cak.rdr-review" }
    }));
    let d = RdrReviewEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Modify);
    assert_eq!(d.violations[0].id, "RR2");
}

#[test]
fn rr3_blocks_insufficient_trace_corpus() {
    for status in [
        "candidate_only",
        "insufficient",
        "fail",
        "unknown",
        "pending",
    ] {
        let req = request(json!({
            "schema_version": "0.1.0",
            "host": { "name": "h", "mode": "ci" },
            "task": { "kind": "review" },
            "state": { "trace_plan_status": status },
            "proposed_action": { "kind": "accept_trace_corpus" },
            "skill": { "id": "cak.rdr-review" }
        }));
        let d = RdrReviewEvaluator.evaluate(&req);
        assert_eq!(d.decision, DecisionKind::Block, "status {status}");
        assert_eq!(d.violations[0].id, "RR3");
    }
}

#[test]
fn rr3_blocks_missing_trace_plan_status() {
    let req = request(json!({
        "schema_version": "0.1.0",
        "host": { "name": "h", "mode": "ci" },
        "task": { "kind": "review" },
        "proposed_action": { "kind": "accept_trace_corpus" },
        "skill": { "id": "cak.rdr-review" }
    }));
    let d = RdrReviewEvaluator.evaluate(&req);
    assert_eq!(d.decision, DecisionKind::Block);
    assert_eq!(d.violations[0].id, "RR3");
    assert_eq!(d.violations[0].actual.as_deref(), Some("unknown"));
}

#[test]
fn rr3_allows_sufficient_trace_corpus() {
    for status in ["sufficient", "pass"] {
        let req = request(json!({
            "schema_version": "0.1.0",
            "host": { "name": "h", "mode": "ci" },
            "task": { "kind": "review" },
            "state": { "trace_plan_status": status },
            "proposed_action": { "kind": "accept_trace_corpus" },
            "skill": { "id": "cak.rdr-review" }
        }));
        assert_allow(&RdrReviewEvaluator.evaluate(&req));
    }
}
