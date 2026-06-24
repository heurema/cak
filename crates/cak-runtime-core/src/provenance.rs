//! Provenance context: evidence pointers (SkillWiki-derived).
//!
//! v0 carries provenance references for audit/trace purposes only. No rule
//! branches on these yet; they exist so decisions can cite evidence and so the
//! contract is stable before provenance-aware gates arrive.

use serde::{Deserialize, Serialize};

/// References linking a request to its supporting evidence artifacts.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProvenanceContext {
    #[serde(default)]
    pub source_refs: Vec<String>,
    #[serde(default)]
    pub trace_refs: Vec<String>,
    #[serde(default)]
    pub diagnosis_refs: Vec<String>,
    #[serde(default)]
    pub preserve_refs: Vec<String>,
}
