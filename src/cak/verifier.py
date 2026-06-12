"""Pre-execution verifier: typed proposal -> explainable decision.

Embeddable by design (docs/17 form-factor hedge): no transport, no IO —
a pure function over GatewayConfig. The gateway, an Envoy ext_proc shim, or
tests call the same entry point.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .predicates import Truth, evaluate_all
from .specs import GatewayConfig

# Strictest-wins ordering for fired policies (sandbox_only/quarantine are
# handled as block in v0.1 — no sandbox runtime yet; recorded in reasons).
_SEVERITY = {
    "allow": 0,
    "warn": 1,
    "require_approval": 2,
    "block": 3,
    "sandbox_only": 3,
    "quarantine": 3,
}
_FINAL = {"sandbox_only": "block", "quarantine": "block"}


@dataclass(frozen=True, slots=True)
class Proposal:
    identity: str
    action: str
    arguments: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Decision:
    """The five-line audit answer of docs/13, as one typed object."""

    action: str
    enforcement: str
    effect_id: str | None
    risk: str | None
    reversibility: str | None
    capability_ok: bool
    fired_policies: tuple[str, ...]
    reasons: tuple[str, ...]
    precondition_unknowns: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def verify(config: GatewayConfig, proposal: Proposal) -> Decision:
    reasons: list[str] = []

    if not config.allowed(proposal.identity, proposal.action):
        return Decision(
            action=proposal.action,
            enforcement="block",
            effect_id=None,
            risk=None,
            reversibility=None,
            capability_ok=False,
            fired_policies=(),
            reasons=(f"identity '{proposal.identity}' has no capability for "
                     f"'{proposal.action}'",),
        )

    action_spec = config.actions.get(proposal.action)
    if action_spec is None:
        return Decision(
            action=proposal.action,
            enforcement="block",
            effect_id=None,
            risk=None,
            reversibility=None,
            capability_ok=True,
            fired_policies=(),
            reasons=(f"no ActionSpec declared for '{proposal.action}'",),
        )

    missing = [p for p in action_spec.required_params if p not in proposal.arguments]
    if missing:
        return Decision(
            action=proposal.action,
            enforcement="block",
            effect_id=None,
            risk=None,
            reversibility=None,
            capability_ok=True,
            fired_policies=(),
            reasons=(f"missing required params: {', '.join(missing)}",),
        )

    effect = config.effects_by_action.get(proposal.action)
    unknowns: list[str] = []
    if effect is not None:
        results = evaluate_all(list(effect.preconditions), proposal.arguments)
        failed = [p for p, truth in results.items() if truth is Truth.FALSE]
        unknowns = [p for p, truth in results.items() if truth is Truth.UNKNOWN]
        if failed:
            return Decision(
                action=proposal.action,
                enforcement="block",
                effect_id=effect.id,
                risk=effect.risk,
                reversibility=effect.reversibility,
                capability_ok=True,
                fired_policies=(),
                reasons=tuple(f"precondition failed: {p}" for p in failed),
                precondition_unknowns=tuple(unknowns),
            )
        if unknowns:
            reasons.append(f"preconditions not evaluable at boundary: {len(unknowns)}")
    else:
        reasons.append(f"no EffectSpec for '{proposal.action}': treating risk as unclassified")

    fired: list[str] = []
    enforcement = "allow"
    for policy in config.policies:
        if not policy.applies_to(proposal.action):
            continue
        results = evaluate_all(list(policy.when), proposal.arguments)
        # Empty `when` = unconditional (logical AND over the empty set):
        # an action-scoped policy with no predicates always fires for its
        # actions. Both cold drafters in exp-004 assumed this independently.
        if all(truth is Truth.TRUE for truth in results.values()):
            fired.append(policy.id)
            reasons.append(f"policy '{policy.id}' fired -> {policy.enforcement}")
            if _SEVERITY[policy.enforcement] > _SEVERITY[enforcement]:
                enforcement = policy.enforcement

    return Decision(
        action=proposal.action,
        enforcement=_FINAL.get(enforcement, enforcement),
        effect_id=effect.id if effect else None,
        risk=effect.risk if effect else None,
        reversibility=effect.reversibility if effect else None,
        capability_ok=True,
        fired_policies=tuple(fired),
        reasons=tuple(reasons),
        precondition_unknowns=tuple(unknowns),
    )
