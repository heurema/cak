//! Output model: a [`Decision`].
//!
//! A `Decision` is the only thing the engine returns. It is a domain verdict,
//! not a process result: `decision == block` is a perfectly valid, successful
//! evaluation — see the CLI exit-code policy in `cak-runtime-cli`.

use serde::{Deserialize, Serialize};

/// The verdict produced for one [`crate::request::EvalRequest`].
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Decision {
    pub schema_version: String,
    pub decision: DecisionKind,
    pub severity: Severity,
    pub reason: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub selected_evaluator: Option<String>,
    #[serde(default)]
    pub violations: Vec<Violation>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub repair: Option<Repair>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub trace: Option<TraceEvent>,
}

/// What the host should do with the proposed action.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DecisionKind {
    Allow,
    Block,
    Modify,
    InjectContext,
    Ask,
    VerifyOnly,
}

impl DecisionKind {
    /// Priority used by the composite resolver. Higher wins.
    ///
    /// `block > ask > modify > inject_context > verify_only > allow`.
    #[must_use]
    pub fn priority(self) -> u8 {
        match self {
            DecisionKind::Block => 5,
            DecisionKind::Ask => 4,
            DecisionKind::Modify => 3,
            DecisionKind::InjectContext => 2,
            DecisionKind::VerifyOnly => 1,
            DecisionKind::Allow => 0,
        }
    }
}

/// How strong the verdict is. Used as a secondary resolver key.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Severity {
    Info,
    Soft,
    Hard,
}

impl Severity {
    /// Priority used by the composite resolver. Higher wins.
    ///
    /// `hard > soft > info`.
    #[must_use]
    pub fn priority(self) -> u8 {
        match self {
            Severity::Hard => 2,
            Severity::Soft => 1,
            Severity::Info => 0,
        }
    }
}

/// A single concrete reason the action failed a gate.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Violation {
    pub id: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub expected: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub actual: Option<String>,
    #[serde(default)]
    pub evidence_refs: Vec<String>,
}

/// A suggested, host-applied remediation. The engine never applies it itself.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Repair {
    pub kind: RepairKind,
    pub text: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub replacement_action: Option<serde_json::Value>,
}

/// The category of remediation a [`Repair`] proposes.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RepairKind {
    ModifyMessage,
    InjectContext,
    RunVerifier,
    KeepDraft,
    SupplyRollback,
    MarkCandidateOnly,
    RequestConfirmation,
    None,
}

/// An audit record describing the verdict, for host trace logs.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TraceEvent {
    pub record: bool,
    pub event: String,
    #[serde(default)]
    pub tags: Vec<String>,
}

impl Decision {
    /// A neutral `allow` with the given reason, trace, and no evaluator stamp.
    #[must_use]
    pub fn allow(reason: impl Into<String>, trace: TraceEvent) -> Self {
        Decision {
            schema_version: crate::SCHEMA_VERSION.to_string(),
            decision: DecisionKind::Allow,
            severity: Severity::Info,
            reason: reason.into(),
            selected_evaluator: None,
            violations: Vec::new(),
            repair: None,
            trace: Some(trace),
        }
    }
}
