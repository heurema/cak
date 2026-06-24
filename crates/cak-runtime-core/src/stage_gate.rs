//! Stage gate (HMT/AWM-derived): keep stage-bound actions aligned with the
//! workflow's reported stage status.
//!
//! With no stage context, the gate allows.

use crate::decision::{
    Decision, DecisionKind, Repair, RepairKind, Severity, TraceEvent, Violation,
};
use crate::evaluator::Evaluator;
use crate::request::EvalRequest;
use crate::stage::StageStatus;

/// Stable evaluator name.
pub const NAME: &str = "stage_gate";

/// Action kinds whose correctness depends on the current stage.
const STAGE_BOUND_KINDS: [&str; 3] = [
    "complete_workflow",
    "execute_stage_bound_action",
    "mark_ready",
];

/// Gate for stage-bound actions against [`StageStatus`].
#[derive(Debug, Default, Clone, Copy)]
pub struct StageGateEvaluator;

fn allow() -> Decision {
    Decision::allow(
        "No stage rule applies to the proposed action.",
        TraceEvent {
            record: true,
            event: "stage_gate.allow".to_string(),
            tags: vec!["stage_gate".to_string(), "allow".to_string()],
        },
    )
}

impl Evaluator for StageGateEvaluator {
    fn name(&self) -> &'static str {
        NAME
    }

    fn evaluate(&self, request: &EvalRequest) -> Decision {
        let Some(stage) = request.stage.as_ref() else {
            return allow();
        };
        let kind = request.proposed_action.kind.as_str();

        // SG1: a stage-bound action while the stage is in mismatch is a hard
        // block.
        if STAGE_BOUND_KINDS.contains(&kind) && stage.stage_status == StageStatus::Mismatch {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: "Stage mismatch: the workflow is not at the expected stage.".to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "SG1".to_string(),
                    expected: stage.expected_stage.clone(),
                    actual: stage.current_stage.clone(),
                    evidence_refs: Vec::new(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::None,
                    text: "Realign to the expected stage before completing this action."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "stage_gate.mismatch_blocked".to_string(),
                    tags: vec![
                        "stage_gate".to_string(),
                        "SG1".to_string(),
                        "mismatch".to_string(),
                    ],
                }),
            };
        }

        // SG2: completing or executing a stage-bound action while
        // preconditions are missing needs confirmation (soft ask).
        if matches!(kind, "complete_workflow" | "execute_stage_bound_action")
            && stage.stage_status == StageStatus::PreconditionsMissing
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Ask,
                severity: Severity::Soft,
                reason: "Stage preconditions are not satisfied yet.".to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "SG2".to_string(),
                    expected: Some("preconditions satisfied".to_string()),
                    actual: Some("preconditions_missing".to_string()),
                    evidence_refs: Vec::new(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RequestConfirmation,
                    text: "Satisfy the stage preconditions or confirm before proceeding."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "stage_gate.preconditions_ask".to_string(),
                    tags: vec![
                        "stage_gate".to_string(),
                        "SG2".to_string(),
                        "preconditions_missing".to_string(),
                    ],
                }),
            };
        }

        allow()
    }
}
