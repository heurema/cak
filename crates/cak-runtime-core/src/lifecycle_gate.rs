//! Lifecycle gate (PSN-derived): protect the skill graph from unsafe
//! activations and ungated updates.
//!
//! Target-skill lookup: use `proposed_action.skill_id` if present, otherwise
//! `request.skill.id`; resolve it against `skill_graph.nodes`. With no graph or
//! no matching node, the gate allows — it never invents lifecycle facts.

use crate::decision::{
    Decision, DecisionKind, Repair, RepairKind, Severity, TraceEvent, Violation,
};
use crate::evaluator::Evaluator;
use crate::request::{AuthorityMode, EvalRequest};
use crate::skill_graph::{Maturity, SkillNode};

/// Stable evaluator name.
pub const NAME: &str = "lifecycle_gate";

/// Gate for skill activation and update against lifecycle maturity.
#[derive(Debug, Default, Clone, Copy)]
pub struct LifecycleGateEvaluator;

fn target_node(request: &EvalRequest) -> Option<&SkillNode> {
    let target_id = request
        .proposed_action
        .skill_id
        .as_deref()
        .unwrap_or(request.skill.id.as_str());
    request.skill_graph.as_ref()?.node(target_id)
}

fn allow() -> Decision {
    Decision::allow(
        "No lifecycle rule applies to the proposed action.",
        TraceEvent {
            record: true,
            event: "lifecycle_gate.allow".to_string(),
            tags: vec!["lifecycle_gate".to_string(), "allow".to_string()],
        },
    )
}

impl Evaluator for LifecycleGateEvaluator {
    fn name(&self) -> &'static str {
        NAME
    }

    fn evaluate(&self, request: &EvalRequest) -> Decision {
        let action = &request.proposed_action;
        let Some(node) = target_node(request) else {
            return allow();
        };
        let maturity = node.lifecycle.maturity;

        // LG1: activating a quarantined/deprecated skill is a hard block.
        if action.kind == "activate_skill"
            && matches!(maturity, Maturity::Quarantined | Maturity::Deprecated)
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: format!(
                    "Skill '{}' is {} and must not be activated.",
                    node.id,
                    maturity_label(maturity)
                ),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "LG1".to_string(),
                    expected: Some("stable|candidate".to_string()),
                    actual: Some(maturity_label(maturity).to_string()),
                    evidence_refs: node.provenance_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::None,
                    text: "Do not activate a quarantined or deprecated skill.".to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "lifecycle_gate.activation_blocked".to_string(),
                    tags: vec![
                        "lifecycle_gate".to_string(),
                        "LG1".to_string(),
                        maturity_label(maturity).to_string(),
                    ],
                }),
            };
        }

        // LG4: a quarantined/deprecated skill must not claim authoritative
        // control either. Activation and authority are separate host actions,
        // but both would let an unsafe lifecycle state influence execution.
        if action.kind == "claim_authority"
            && matches!(maturity, Maturity::Quarantined | Maturity::Deprecated)
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: format!(
                    "Skill '{}' is {} and must not claim authoritative control.",
                    node.id,
                    maturity_label(maturity)
                ),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "LG4".to_string(),
                    expected: Some("stable|candidate authority claim".to_string()),
                    actual: Some(format!("claim_authority + {}", maturity_label(maturity))),
                    evidence_refs: node.provenance_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::None,
                    text: "Do not grant authority to a quarantined or deprecated skill."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "lifecycle_gate.authority_blocked".to_string(),
                    tags: vec![
                        "lifecycle_gate".to_string(),
                        "LG4".to_string(),
                        maturity_label(maturity).to_string(),
                    ],
                }),
            };
        }

        // LG2: updating a stable/protected skill without a rollback checkpoint
        // is a hard block.
        if action.kind == "update_skill"
            && matches!(maturity, Maturity::Stable | Maturity::Protected)
            && node.lifecycle.rollback_checkpoint.is_none()
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: format!(
                    "Skill '{}' is {} and cannot be updated without a rollback checkpoint.",
                    node.id,
                    maturity_label(maturity)
                ),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "LG2".to_string(),
                    expected: Some("rollback_checkpoint present".to_string()),
                    actual: Some("rollback_checkpoint missing".to_string()),
                    evidence_refs: node.provenance_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::SupplyRollback,
                    text:
                        "Supply a rollback checkpoint before updating a stable or protected skill."
                            .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "lifecycle_gate.update_blocked".to_string(),
                    tags: vec![
                        "lifecycle_gate".to_string(),
                        "LG2".to_string(),
                        "missing_rollback".to_string(),
                    ],
                }),
            };
        }

        // LG3: claiming authoritative control with an immature skill needs
        // confirmation (soft ask).
        if matches!(action.kind.as_str(), "activate_skill" | "claim_authority")
            && action.authority == Some(AuthorityMode::Authoritative)
            && matches!(maturity, Maturity::Draft | Maturity::Candidate)
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Ask,
                severity: Severity::Soft,
                reason: format!(
                    "Skill '{}' is {}; authoritative control needs confirmation.",
                    node.id,
                    maturity_label(maturity)
                ),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "LG3".to_string(),
                    expected: Some("advisory or stable+authoritative".to_string()),
                    actual: Some(format!("authoritative + {}", maturity_label(maturity))),
                    evidence_refs: node.provenance_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RequestConfirmation,
                    text: "Confirm before granting an immature skill authoritative control, or keep it advisory."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "lifecycle_gate.authority_ask".to_string(),
                    tags: vec![
                        "lifecycle_gate".to_string(),
                        "LG3".to_string(),
                        maturity_label(maturity).to_string(),
                    ],
                }),
            };
        }

        allow()
    }
}

fn maturity_label(maturity: Maturity) -> &'static str {
    match maturity {
        Maturity::Draft => "draft",
        Maturity::Candidate => "candidate",
        Maturity::Stable => "stable",
        Maturity::Protected => "protected",
        Maturity::Deprecated => "deprecated",
        Maturity::Quarantined => "quarantined",
    }
}
