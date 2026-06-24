//! Serde roundtrip coverage for the request and decision contracts.

use cak_runtime_core::{evaluate, Decision, EvalRequest};
use pretty_assertions::assert_eq;
use serde_json::json;

/// A maximally-populated request: every optional context present.
fn full_request_json() -> serde_json::Value {
    json!({
        "schema_version": "0.1.0",
        "request_id": "roundtrip-1",
        "host": { "name": "cak-host", "mode": "plugin", "version": "0.1.0" },
        "task": { "kind": "activate_skill", "goal": "exercise every field" },
        "state": { "decision_packet_status": "exploratory", "c10_status": "hypothesis_level" },
        "artifacts": { "pr": "pr/10" },
        "proposed_action": {
            "kind": "activate_skill",
            "text": "activate the resolver",
            "target": "skill.resolve_entity",
            "skill_id": "skill.resolve_entity",
            "authority": "authoritative",
            "args": { "force": false }
        },
        "skill": { "id": "cak.host-loader", "version": "0.1.0" },
        "skill_graph": {
            "nodes": [
                {
                    "id": "skill.resolve_entity",
                    "kind": "intervention",
                    "version": "0.4.0",
                    "lifecycle": {
                        "maturity": "candidate",
                        "health": "degraded",
                        "rollback_checkpoint": "ckpt.7",
                        "quarantine_reason": null
                    },
                    "provenance_refs": ["trace.1"]
                }
            ],
            "edges": [
                { "from": "skill.resolve_entity", "to": "skill.verify_unique", "kind": "verifies" }
            ]
        },
        "stage": {
            "intent": "resolve_place_entity",
            "current_stage": "search",
            "expected_stage": "verify_unique",
            "stage_status": "active"
        },
        "proof": {
            "verifier_status": "passed",
            "grounding_status": "grounded",
            "proof_obligations": ["entity_unique"],
            "counterexample_refs": ["cx.1"]
        },
        "provenance": {
            "source_refs": ["paper.hasp"],
            "trace_refs": ["trace.1"],
            "diagnosis_refs": ["diag.1"],
            "preserve_refs": ["preserve.1"]
        },
        "metadata": { "origin": "test" }
    })
}

#[test]
fn eval_request_roundtrips_through_value() {
    let parsed: EvalRequest = serde_json::from_value(full_request_json()).expect("request parses");
    let value = serde_json::to_value(&parsed).expect("request serializes");
    let reparsed: EvalRequest = serde_json::from_value(value).expect("request re-parses");
    assert_eq!(parsed, reparsed);
}

#[test]
fn eval_request_applies_defaults_for_optional_fields() {
    // Minimal request: defaults must fill state/artifacts/metadata with `{}`
    // and leave the optional contexts absent.
    let minimal = json!({
        "schema_version": "0.1.0",
        "host": { "name": "cak-host", "mode": "cli" },
        "task": { "kind": "edit_docs" },
        "proposed_action": { "kind": "edit_file" },
        "skill": { "id": "cak.docs-helper" }
    });
    let parsed: EvalRequest = serde_json::from_value(minimal).expect("minimal request parses");

    assert!(parsed.state.is_object());
    assert!(parsed.artifacts.is_object());
    assert!(parsed.metadata.is_object());
    assert!(parsed.proposed_action.args.is_object());
    assert!(parsed.skill_graph.is_none());
    assert!(parsed.stage.is_none());
    assert!(parsed.proof.is_none());
    assert!(parsed.provenance.is_none());
    assert!(parsed.request_id.is_none());
}

#[test]
fn decision_roundtrips_through_value() {
    let request: EvalRequest = serde_json::from_value(full_request_json()).expect("request parses");
    let decision = evaluate(&request);

    let value = serde_json::to_value(&decision).expect("decision serializes");
    let reparsed: Decision = serde_json::from_value(value).expect("decision re-parses");
    assert_eq!(decision, reparsed);
}
