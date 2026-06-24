//! CAK Runtime v0 core — a host-neutral decision engine.
//!
//! The entire boundary is `EvalRequest -> Decision`. Given an in-memory
//! [`EvalRequest`], the engine returns a [`Decision`]. That is all it does.
//!
//! What this crate is **not**, by design:
//!
//! - it is not an agent framework and does not own the agent loop;
//! - it does not parse markdown, read GitHub, or inspect the filesystem;
//! - it never shells out, opens a socket, or touches repository state;
//! - it does not execute skill scripts, implement MCP, or admit skills.
//!
//! Every fact the engine uses must be present in the request JSON. If a fact is
//! not in the request, it does not exist for the evaluator. This keeps the core
//! deterministic, pure, and trivially testable: a `Decision` is a function of an
//! `EvalRequest` and nothing else.

pub mod composite;
pub mod decision;
pub mod evaluator;
pub mod lifecycle_gate;
pub mod proof;
pub mod proof_gate;
pub mod provenance;
pub mod rdr_review;
pub mod request;
pub mod skill_graph;
pub mod stage;
pub mod stage_gate;

pub use composite::{evaluate, CompositeEvaluator};
pub use decision::{Decision, DecisionKind, Repair, RepairKind, Severity, TraceEvent, Violation};
pub use evaluator::Evaluator;
pub use request::EvalRequest;

/// Schema version stamped onto every [`Decision`] this crate produces, and the
/// version the bundled fixtures are written against.
pub const SCHEMA_VERSION: &str = "0.1.0";

/// Errors surfaced by the core's convenience helpers.
///
/// The core itself is infallible during evaluation; the only fallible step is
/// turning untrusted JSON into a typed [`EvalRequest`].
#[derive(Debug, thiserror::Error)]
pub enum CoreError {
    /// The input was not a well-formed [`EvalRequest`].
    #[error("failed to parse EvalRequest JSON: {0}")]
    Parse(#[from] serde_json::Error),
}

/// Parse an [`EvalRequest`] from a JSON string.
///
/// # Errors
///
/// Returns [`CoreError::Parse`] if the JSON is malformed or does not match the
/// [`EvalRequest`] shape.
pub fn parse_request(json: &str) -> Result<EvalRequest, CoreError> {
    Ok(serde_json::from_str(json)?)
}
