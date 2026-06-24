//! Skill-graph context: nodes, edges, and lifecycle state.
//!
//! v0 carries a minimal, host-supplied graph. The engine only *reads* it to
//! look up the lifecycle state of a target skill; it never mutates the graph,
//! resolves it from disk, or performs admission.

use serde::{Deserialize, Serialize};

/// The slice of the skill graph relevant to this request.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SkillGraphContext {
    #[serde(default)]
    pub nodes: Vec<SkillNode>,
    #[serde(default)]
    pub edges: Vec<SkillEdge>,
}

impl SkillGraphContext {
    /// Find a node by id.
    #[must_use]
    pub fn node(&self, id: &str) -> Option<&SkillNode> {
        self.nodes.iter().find(|node| node.id == id)
    }
}

/// One skill in the graph, with its lifecycle and provenance pointers.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SkillNode {
    pub id: String,
    pub kind: SkillKind,
    pub version: String,
    pub lifecycle: LifecycleFields,
    #[serde(default)]
    pub provenance_refs: Vec<String>,
}

/// The structural category of a skill node.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SkillKind {
    Contract,
    Intervention,
    Workflow,
    Stage,
    Verifier,
    Package,
    Hybrid,
}

/// A directed relationship between two skill nodes.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SkillEdge {
    pub from: String,
    pub to: String,
    pub kind: EdgeKind,
}

/// The kind of relationship a [`SkillEdge`] expresses.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EdgeKind {
    DependsOn,
    Calls,
    ConflictsWith,
    Repairs,
    Verifies,
    DerivedFrom,
}

/// Lifecycle state attached to a skill node.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LifecycleFields {
    pub maturity: Maturity,
    pub health: Health,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub rollback_checkpoint: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub quarantine_reason: Option<String>,
}

/// Maturity ladder for a skill. Gates branch on these states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Maturity {
    Draft,
    Candidate,
    Stable,
    Protected,
    Deprecated,
    Quarantined,
}

/// Observed health of a skill from replay/verifier signals.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Health {
    Unknown,
    Healthy,
    FailedReplay,
    FailedVerifier,
    Degraded,
}
