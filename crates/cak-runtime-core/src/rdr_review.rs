//! RDR review gate: domain rules for CAK R&D pull requests and research
//! packets. Encodes the RDR-001 readiness and overclaim guards as executable
//! decisions.
//!
//! All facts come from `state` in the request (host-supplied), never from the
//! repository. With none of the rules matching, the gate allows.

use crate::decision::{
    Decision, DecisionKind, Repair, RepairKind, Severity, TraceEvent, Violation,
};
use crate::evaluator::Evaluator;
use crate::request::EvalRequest;

/// Stable evaluator name.
pub const NAME: &str = "rdr_review";

/// Trace-plan statuses that are not sufficient to accept a trace corpus.
const INSUFFICIENT_TRACE_STATUSES: [&str; 3] = ["candidate_only", "insufficient", "fail"];

/// Gate for CAK R&D research-packet readiness and claim discipline.
#[derive(Debug, Default, Clone, Copy)]
pub struct RdrReviewEvaluator;

fn state_str<'a>(request: &'a EvalRequest, key: &str) -> Option<&'a str> {
    request.state.get(key).and_then(serde_json::Value::as_str)
}

fn allow() -> Decision {
    Decision::allow(
        "No RDR review rule applies to the proposed action.",
        TraceEvent {
            record: true,
            event: "rdr_review.allow".to_string(),
            tags: vec!["rdr_review".to_string(), "allow".to_string()],
        },
    )
}

impl Evaluator for RdrReviewEvaluator {
    fn name(&self) -> &'static str {
        NAME
    }

    fn evaluate(&self, request: &EvalRequest) -> Decision {
        let action = &request.proposed_action;
        let kind = action.kind.as_str();

        // RR1: recommending merge / marking ready while the decision packet is
        // not decision-ready is a hard block.
        if matches!(kind, "recommend_merge" | "mark_ready")
            && state_str(request, "decision_packet_status") != Some("decision_ready")
        {
            let actual = state_str(request, "decision_packet_status")
                .unwrap_or("unknown")
                .to_string();
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: "Research packet is not decision-ready.".to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "RR1".to_string(),
                    expected: Some("decision_ready".to_string()),
                    actual: Some(actual),
                    evidence_refs: Vec::new(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::KeepDraft,
                    text: "Keep the PR in draft until the decision packet is decision-ready."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "rdr_review.merge_blocked".to_string(),
                    tags: vec![
                        "rdr_review".to_string(),
                        "RR1".to_string(),
                        "not_decision_ready".to_string(),
                    ],
                }),
            };
        }

        // RR2: claiming C10 as supported while it is hypothesis-level should be
        // softened to a hypothesis framing (soft modify).
        if kind == "claim_supported"
            && action.text_mentions("C10")
            && state_str(request, "c10_status") == Some("hypothesis_level")
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Modify,
                severity: Severity::Soft,
                reason: "C10 is hypothesis-level synthesis, not a supported architecture decision."
                    .to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "RR2".to_string(),
                    expected: Some("hypothesis-level framing".to_string()),
                    actual: Some("claimed as supported".to_string()),
                    evidence_refs: Vec::new(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::ModifyMessage,
                    text: "Frame C10 as a hypothesis-level synthesis, not a supported architecture decision."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "rdr_review.c10_overclaim_modify".to_string(),
                    tags: vec![
                        "rdr_review".to_string(),
                        "RR2".to_string(),
                        "hypothesis_level".to_string(),
                    ],
                }),
            };
        }

        // RR3: accepting a trace corpus whose plan is not sufficient is a hard
        // block.
        if kind == "accept_trace_corpus" {
            if let Some(status) = state_str(request, "trace_plan_status") {
                if INSUFFICIENT_TRACE_STATUSES.contains(&status) {
                    return Decision {
                        schema_version: crate::SCHEMA_VERSION.to_string(),
                        decision: DecisionKind::Block,
                        severity: Severity::Hard,
                        reason: "Trace corpus plan is not sufficient.".to_string(),
                        selected_evaluator: Some(NAME.to_string()),
                        violations: vec![Violation {
                            id: "RR3".to_string(),
                            expected: Some("sufficient|pass".to_string()),
                            actual: Some(status.to_string()),
                            evidence_refs: Vec::new(),
                        }],
                        repair: Some(Repair {
                            kind: RepairKind::None,
                            text:
                                "Strengthen the trace corpus plan before accepting it as evidence."
                                    .to_string(),
                            replacement_action: None,
                        }),
                        trace: Some(TraceEvent {
                            record: true,
                            event: "rdr_review.trace_corpus_blocked".to_string(),
                            tags: vec![
                                "rdr_review".to_string(),
                                "RR3".to_string(),
                                status.to_string(),
                            ],
                        }),
                    };
                }
            }
        }

        allow()
    }
}
