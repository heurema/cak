"""Semantic replay over a recorded trace (docs/14 semantics).

No live calls, no byte-identical claims. Two checkpoint families:

1. Decision fidelity — re-run the verifier on each recorded proposal against
   the *current* config; the enforcement and fired policies must match the
   recorded decision.
2. Postcondition fidelity — re-evaluate effect `causes` against the recorded
   tool results; truth values must match what was recorded.

A divergence is a finding, not necessarily a failure: it shows that config
or environment changed semantics since the trace was recorded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .predicates import evaluate_all
from .specs import GatewayConfig
from .trace import read_trace
from .verifier import Proposal, verify


@dataclass(slots=True)
class Divergence:
    call_id: Any
    checkpoint: str
    recorded: Any
    replayed: Any


@dataclass(slots=True)
class ReplayReport:
    proposals: int = 0
    decisions_checked: int = 0
    postconditions_checked: int = 0
    divergences: list[Divergence] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.divergences


def _proposal_without_decision(
    proposals: list[dict[str, Any]], call_id: Any
) -> dict[str, Any] | None:
    for proposal in reversed(proposals):
        if proposal.get("call_id") == call_id and "recorded_decision" not in proposal:
            return proposal
    return None


def replay(config: GatewayConfig, trace_path: Path) -> ReplayReport:
    events = read_trace(trace_path)
    report = ReplayReport()

    proposals: list[dict[str, Any]] = []

    for event in events:
        call_id = event.get("call_id")
        if event["type"] == "proposal":
            proposals.append(event)
            report.proposals += 1
        elif event["type"] == "decision":
            proposal = _proposal_without_decision(proposals, call_id)
            if proposal is None:
                report.divergences.append(
                    Divergence(call_id, "decision", "decision without proposal", None)
                )
            else:
                proposal["recorded_decision"] = event["decision"]
        elif event["type"] == "postconditions":
            recorded_checks: dict[str, str] = event["checks"]
            outcome_context = event.get("result_context")
            if outcome_context is not None:
                replayed = {
                    predicate: truth.value
                    for predicate, truth in evaluate_all(
                        list(recorded_checks), outcome_context
                    ).items()
                }
                report.postconditions_checked += 1
                if replayed != recorded_checks:
                    report.divergences.append(
                        Divergence(call_id, "postconditions", recorded_checks, replayed)
                    )

    for proposal_event in proposals:
        call_id = proposal_event.get("call_id")
        recorded = proposal_event.get("recorded_decision")
        if recorded is None:
            report.divergences.append(
                Divergence(call_id, "decision", "missing recorded decision", None)
            )
            continue
        decision = verify(
            config,
            Proposal(
                identity=proposal_event["identity"],
                action=proposal_event["action"],
                arguments=proposal_event["arguments"],
            ),
        )
        report.decisions_checked += 1
        replayed_view = {
            "enforcement": decision.enforcement,
            "fired_policies": list(decision.fired_policies),
        }
        recorded_view = {
            "enforcement": recorded.get("enforcement"),
            "fired_policies": list(recorded.get("fired_policies", [])),
        }
        if replayed_view != recorded_view:
            report.divergences.append(
                Divergence(call_id, "decision", recorded_view, replayed_view)
            )

    return report
