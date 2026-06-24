//! Proof context: verifier and grounding status (VASO-derived).
//!
//! The host runs verifiers and assesses grounding, then reports outcomes here.
//! The engine never executes a verifier; it gates claims against the reported
//! [`VerifierStatus`] and [`GroundingStatus`].

use serde::{Deserialize, Serialize};

/// Verifier/grounding evidence backing a verification claim.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ProofContext {
    pub verifier_status: VerifierStatus,
    pub grounding_status: GroundingStatus,
    #[serde(default)]
    pub proof_obligations: Vec<String>,
    #[serde(default)]
    pub counterexample_refs: Vec<String>,
}

/// Whether the host's verifier has run and what it concluded.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum VerifierStatus {
    NotRun,
    Passed,
    Failed,
}

/// Whether the mapping from runtime state to propositions is trustworthy.
///
/// A passing verifier over bad grounding can approve unsafe behavior (the VASO
/// caution), so grounding is tracked separately from verifier status.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum GroundingStatus {
    Unknown,
    Grounded,
    Suspect,
}
