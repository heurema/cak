//! Host-facing adapter over the CAK runtime.
//!
//! The adapter is the first Rust boundary above `cak-runtime-core`: it accepts
//! a host proposal, evaluates it with the pure runtime, and translates the
//! domain [`Decision`](cak_runtime_core::Decision) into a small outcome enum a
//! host gateway or skill shim can honor before executing an action.

use cak_runtime_core::{Decision, DecisionKind, EvalRequest};
use serde::{Deserialize, Serialize};

/// v0 host proposals deliberately reuse the runtime request shape.
///
/// The host adapter owns the enforcement mapping, not a new schema. A narrower
/// proposal input can be introduced later once real host integrations prove
/// which defaults are stable.
pub type HostProposal = EvalRequest;

/// Host-facing action after runtime evaluation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HostOutcomeKind {
    Proceed,
    Deny,
    NeedsModification,
    InjectContext,
    NeedsConfirmation,
    NeedsVerification,
}

impl HostOutcomeKind {
    #[must_use]
    pub fn from_decision(decision: DecisionKind) -> Self {
        match decision {
            DecisionKind::Allow => HostOutcomeKind::Proceed,
            DecisionKind::Block => HostOutcomeKind::Deny,
            DecisionKind::Modify => HostOutcomeKind::NeedsModification,
            DecisionKind::InjectContext => HostOutcomeKind::InjectContext,
            DecisionKind::Ask => HostOutcomeKind::NeedsConfirmation,
            DecisionKind::VerifyOnly => HostOutcomeKind::NeedsVerification,
        }
    }
}

/// Full adapter result: the host-facing outcome plus the underlying decision.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HostOutcome {
    pub schema_version: String,
    pub outcome: HostOutcomeKind,
    pub decision: Decision,
}

/// Evaluate a host proposal and map the decision into a host outcome.
#[must_use]
pub fn evaluate_proposal(proposal: &HostProposal) -> HostOutcome {
    let decision = cak_runtime_core::evaluate(proposal);
    HostOutcome {
        schema_version: cak_runtime_core::SCHEMA_VERSION.to_string(),
        outcome: HostOutcomeKind::from_decision(decision.decision),
        decision,
    }
}
