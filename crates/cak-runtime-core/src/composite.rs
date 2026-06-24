//! The [`CompositeEvaluator`]: run the four gates and resolve one [`Decision`].
//!
//! Order: Lifecycle -> Stage -> Proof -> RdrReview.
//!
//! Decision priority: `block > ask > modify > inject_context > verify_only > allow`.
//! Severity priority: `hard > soft > info`.
//! Evaluator tie-break (earlier wins): Lifecycle > Stage > Proof > RdrReview.
//!
//! Short-circuit happens only on a `block`/`hard` decision.

use std::cmp::Ordering;

use crate::decision::{Decision, DecisionKind, Severity, TraceEvent};
use crate::evaluator::Evaluator;
use crate::lifecycle_gate::LifecycleGateEvaluator;
use crate::proof_gate::ProofGateEvaluator;
use crate::rdr_review::RdrReviewEvaluator;
use crate::request::EvalRequest;
use crate::stage_gate::StageGateEvaluator;

/// Runs every gate and resolves their decisions into one verdict.
pub struct CompositeEvaluator {
    evaluators: Vec<Box<dyn Evaluator>>,
}

impl Default for CompositeEvaluator {
    fn default() -> Self {
        // Order is significant: it sets both the short-circuit order and the
        // tie-break rank (index = rank, lower wins ties).
        CompositeEvaluator {
            evaluators: vec![
                Box::new(LifecycleGateEvaluator),
                Box::new(StageGateEvaluator),
                Box::new(ProofGateEvaluator),
                Box::new(RdrReviewEvaluator),
            ],
        }
    }
}

/// Does `new` (at `new_rank`) beat the current best `cur` (at `cur_rank`)?
///
/// Primary key: decision priority. Secondary: severity. Tie-break: lower rank.
fn wins(new: &Decision, new_rank: usize, cur: &Decision, cur_rank: usize) -> bool {
    let new_key = (new.decision.priority(), new.severity.priority());
    let cur_key = (cur.decision.priority(), cur.severity.priority());
    match new_key.cmp(&cur_key) {
        Ordering::Greater => true,
        Ordering::Less => false,
        Ordering::Equal => new_rank < cur_rank,
    }
}

fn composite_allow() -> Decision {
    Decision::allow(
        "No gate matched the proposed action.",
        TraceEvent {
            record: true,
            event: "composite.allow".to_string(),
            tags: vec!["composite".to_string(), "allow".to_string()],
        },
    )
}

impl Evaluator for CompositeEvaluator {
    fn name(&self) -> &'static str {
        "composite"
    }

    fn evaluate(&self, request: &EvalRequest) -> Decision {
        let mut best: Option<(usize, Decision)> = None;

        for (rank, evaluator) in self.evaluators.iter().enumerate() {
            let decision = evaluator.evaluate(request);

            // Short-circuit only on a hard block. It is the top of the priority
            // order, and stopping here keeps the earliest hard block as the
            // reported verdict.
            if decision.decision == DecisionKind::Block && decision.severity == Severity::Hard {
                return decision;
            }

            best = Some(match best {
                None => (rank, decision),
                Some((best_rank, best_decision)) => {
                    if wins(&decision, rank, &best_decision, best_rank) {
                        (rank, decision)
                    } else {
                        (best_rank, best_decision)
                    }
                }
            });
        }

        match best {
            Some((_, decision)) if decision.decision != DecisionKind::Allow => decision,
            _ => composite_allow(),
        }
    }
}

/// Evaluate a request with the default composite gate stack.
#[must_use]
pub fn evaluate(request: &EvalRequest) -> Decision {
    CompositeEvaluator::default().evaluate(request)
}
