//! Input model: an in-memory [`EvalRequest`].
//!
//! Runtime v0 is host-neutral. Every fact the engine reasons about must be
//! present in this request. The core crate never inspects the filesystem,
//! network, or repository state to fill gaps — if a fact is not in the JSON,
//! it does not exist for the evaluator.

use serde::{Deserialize, Serialize};

use crate::proof::ProofContext;
use crate::provenance::ProvenanceContext;
use crate::skill_graph::SkillGraphContext;
use crate::stage::StageContext;

/// Default for free-form JSON value fields: an empty object `{}`.
///
/// `serde_json::Value::default()` is `Null`; the v0 contract is `{}`.
fn empty_object() -> serde_json::Value {
    serde_json::Value::Object(serde_json::Map::new())
}

/// A single, fully self-describing evaluation request.
///
/// `EvalRequest -> Decision` is the entire runtime boundary. The host builds
/// this object (from markdown, GitHub, agent state, etc.) and hands it to the
/// engine; the engine returns a [`crate::decision::Decision`] without touching
/// anything outside this struct.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EvalRequest {
    pub schema_version: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub request_id: Option<String>,
    pub host: HostContext,
    pub task: TaskContext,
    #[serde(default = "empty_object")]
    pub state: serde_json::Value,
    #[serde(default = "empty_object")]
    pub artifacts: serde_json::Value,
    pub proposed_action: ProposedAction,
    pub skill: SkillRef,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub skill_graph: Option<SkillGraphContext>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stage: Option<StageContext>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub proof: Option<ProofContext>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub provenance: Option<ProvenanceContext>,
    #[serde(default = "empty_object")]
    pub metadata: serde_json::Value,
}

/// Where the request originates and in what execution mode.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HostContext {
    pub name: String,
    pub mode: HostMode,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub version: Option<String>,
}

/// Host execution surfaces. Informational in v0 — no rule branches on it yet.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum HostMode {
    Cli,
    Plugin,
    Mcp,
    Ci,
    Test,
}

/// What the agent is broadly trying to do.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TaskContext {
    pub kind: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub goal: Option<String>,
}

/// The concrete next transition the agent proposes. This is what gets gated.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProposedAction {
    pub kind: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub target: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub skill_id: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub authority: Option<AuthorityMode>,
    #[serde(default = "empty_object")]
    pub args: serde_json::Value,
}

/// Whether a skill claims advisory or authoritative control over the transition.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum AuthorityMode {
    Advisory,
    Authoritative,
}

/// The skill on whose behalf the request is evaluated.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SkillRef {
    pub id: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub version: Option<String>,
}

impl ProposedAction {
    /// Case-insensitive substring check over [`ProposedAction::text`].
    ///
    /// Returns `false` when there is no text. Used by prose-sensitive rules
    /// (e.g. proof grounding) without any markdown parsing — it is a plain
    /// substring test over the already-extracted text the host supplied.
    #[must_use]
    pub fn text_mentions(&self, needle: &str) -> bool {
        match &self.text {
            Some(text) => text.to_lowercase().contains(&needle.to_lowercase()),
            None => false,
        }
    }
}
