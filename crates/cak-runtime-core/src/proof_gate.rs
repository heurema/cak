//! Proof gate (VASO-derived): a verification claim must be backed by a passing
//! verifier and trustworthy grounding.
//!
//! With no proof context, the gate allows. PG1 (block) always wins over the
//! softer PG2/PG3 signals.

use crate::decision::{
    Decision, DecisionKind, Repair, RepairKind, Severity, TraceEvent, Violation,
};
use crate::evaluator::Evaluator;
use crate::proof::{GroundingStatus, VerifierStatus};
use crate::request::EvalRequest;

/// Stable evaluator name.
pub const NAME: &str = "proof_gate";

/// Action kinds that assert a verification result.
const CLAIM_KINDS: [&str; 3] = ["claim_verified", "mark_verified", "accept_proof"];

/// Gate for verification claims against verifier and grounding status.
#[derive(Debug, Default, Clone, Copy)]
pub struct ProofGateEvaluator;

fn allow() -> Decision {
    Decision::allow(
        "No proof rule applies to the proposed action.",
        TraceEvent {
            record: true,
            event: "proof_gate.allow".to_string(),
            tags: vec!["proof_gate".to_string(), "allow".to_string()],
        },
    )
}

impl Evaluator for ProofGateEvaluator {
    fn name(&self) -> &'static str {
        NAME
    }

    fn evaluate(&self, request: &EvalRequest) -> Decision {
        let Some(proof) = request.proof.as_ref() else {
            return allow();
        };
        let action = &request.proposed_action;
        let kind = action.kind.as_str();
        let is_claim = CLAIM_KINDS.contains(&kind);

        // PG1: a verification claim without a passing verifier is a hard block.
        // This wins over every softer proof signal.
        if is_claim && proof.verifier_status != VerifierStatus::Passed {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: "Verification claimed but the verifier has not passed.".to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "PG1".to_string(),
                    expected: Some("verifier_status=passed".to_string()),
                    actual: Some(verifier_label(proof.verifier_status).to_string()),
                    evidence_refs: proof.counterexample_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RunVerifier,
                    text:
                        "Run the verifier and obtain a passing result before claiming verification."
                            .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "proof_gate.unverified_claim_blocked".to_string(),
                    tags: vec![
                        "proof_gate".to_string(),
                        "PG1".to_string(),
                        verifier_label(proof.verifier_status).to_string(),
                    ],
                }),
            };
        }

        // PG2: a verification claim whose verifier passed but whose grounding is
        // unknown/suspect should re-verify grounding (soft verify_only).
        if is_claim
            && matches!(
                proof.grounding_status,
                GroundingStatus::Unknown | GroundingStatus::Suspect
            )
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::VerifyOnly,
                severity: Severity::Soft,
                reason: "Verifier passed but grounding is not established.".to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "PG2".to_string(),
                    expected: Some("grounding_status=grounded".to_string()),
                    actual: Some(grounding_label(proof.grounding_status).to_string()),
                    evidence_refs: Vec::new(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RunVerifier,
                    text: "Establish grounding before accepting the verification claim."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "proof_gate.grounding_verify_only".to_string(),
                    tags: vec![
                        "proof_gate".to_string(),
                        "PG2".to_string(),
                        grounding_label(proof.grounding_status).to_string(),
                    ],
                }),
            };
        }

        // PG4: prose that asserts support/verification after a failed verifier
        // is a hard block even when the action kind is not an explicit claim.
        if (action.text_mentions("verified") || action.text_mentions("supported"))
            && proof.verifier_status == VerifierStatus::Failed
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::Block,
                severity: Severity::Hard,
                reason: "Text asserts verification even though the verifier failed."
                    .to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "PG4".to_string(),
                    expected: Some("verifier_status=passed".to_string()),
                    actual: Some("failed".to_string()),
                    evidence_refs: proof.counterexample_refs.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RunVerifier,
                    text: "Do not claim support after a failed verifier; resolve the counterexamples first."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "proof_gate.failed_text_claim_blocked".to_string(),
                    tags: vec![
                        "proof_gate".to_string(),
                        "PG4".to_string(),
                        "failed".to_string(),
                    ],
                }),
            };
        }

        // PG3: prose that asserts "verified"/"supported" while obligations
        // remain and the verifier has not run should re-verify (soft
        // verify_only). PG1 already covers the explicit claim kinds.
        if (action.text_mentions("verified") || action.text_mentions("supported"))
            && !proof.proof_obligations.is_empty()
            && proof.verifier_status == VerifierStatus::NotRun
        {
            return Decision {
                schema_version: crate::SCHEMA_VERSION.to_string(),
                decision: DecisionKind::VerifyOnly,
                severity: Severity::Soft,
                reason: "Text asserts verification while proof obligations are unmet and the verifier has not run."
                    .to_string(),
                selected_evaluator: Some(NAME.to_string()),
                violations: vec![Violation {
                    id: "PG3".to_string(),
                    expected: Some("verifier_status=passed".to_string()),
                    actual: Some("not_run".to_string()),
                    evidence_refs: proof.proof_obligations.clone(),
                }],
                repair: Some(Repair {
                    kind: RepairKind::RunVerifier,
                    text: "Run the verifier to discharge the open proof obligations before claiming support."
                        .to_string(),
                    replacement_action: None,
                }),
                trace: Some(TraceEvent {
                    record: true,
                    event: "proof_gate.text_overclaim_verify_only".to_string(),
                    tags: vec![
                        "proof_gate".to_string(),
                        "PG3".to_string(),
                        "obligations_open".to_string(),
                    ],
                }),
            };
        }

        allow()
    }
}

fn verifier_label(status: VerifierStatus) -> &'static str {
    match status {
        VerifierStatus::NotRun => "not_run",
        VerifierStatus::Passed => "passed",
        VerifierStatus::Failed => "failed",
    }
}

fn grounding_label(status: GroundingStatus) -> &'static str {
    match status {
        GroundingStatus::Unknown => "unknown",
        GroundingStatus::Grounded => "grounded",
        GroundingStatus::Suspect => "suspect",
    }
}
