//! The [`Evaluator`] trait: one gate over an [`EvalRequest`].
//!
//! Every gate is a pure function of the request. No evaluator performs I/O,
//! spawns processes, or reaches the network — this is enforced by construction
//! (they only receive `&EvalRequest`) and asserted by the crate's tests.

use crate::decision::Decision;
use crate::request::EvalRequest;

/// A single decision gate.
pub trait Evaluator {
    /// Stable identifier, used as `selected_evaluator` and for tie-breaking.
    fn name(&self) -> &'static str;

    /// Evaluate the request and return a [`Decision`]. A gate that does not
    /// apply returns a neutral `allow`.
    fn evaluate(&self, request: &EvalRequest) -> Decision;
}
