//! Stage context: stage-aware workflow state (HMT/AWM-derived).
//!
//! The host computes stage alignment and reports the result. The engine does
//! not run a planner; it only reacts to the reported [`StageStatus`].

use serde::{Deserialize, Serialize};

/// Reported alignment between the agent and the workflow's expected stage.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct StageContext {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub intent: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub current_stage: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub expected_stage: Option<String>,
    pub stage_status: StageStatus,
}

/// Status of the current stage relative to its pre/postconditions.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum StageStatus {
    Unknown,
    PreconditionsMissing,
    Active,
    PostconditionsSatisfied,
    Mismatch,
}
