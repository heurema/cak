"""Typed state primitives for ContractSpec checks.

The contract checker intentionally uses a small, explicit state slice rather than
trying to model the full world. Grounding code can populate `facts` from traces,
verifiers, gateway state, approval records, or tool observations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .verifier import Proposal


@dataclass(frozen=True, slots=True)
class TypeAtom:
    """A lightweight type assertion about a subject in agent state."""

    family: str
    state: str
    subject: str | None = None


@dataclass(frozen=True, slots=True)
class TypedState:
    """The checkable subset of agent state used by ContractSpec.

    `facts` is the intentionally boring predicate context. `atoms` is a compact
    future-facing type lattice surface; the current MVP exposes atoms through
    helper methods while contract predicates primarily evaluate over `facts`.
    """

    atoms: tuple[TypeAtom, ...] = ()
    facts: dict[str, Any] = field(default_factory=dict)

    def has_atom(self, family: str, state: str, subject: str | None = None) -> bool:
        return any(
            atom.family == family
            and atom.state == state
            and (subject is None or atom.subject == subject)
            for atom in self.atoms
        )

    def to_context(self, proposal: Proposal) -> dict[str, Any]:
        """Build a predicate context for contract matching and requirements."""
        context: dict[str, Any] = dict(self.facts)
        context.setdefault(
            "proposal",
            {
                "identity": proposal.identity,
                "action": proposal.action,
                "arguments": proposal.arguments,
            },
        )
        context.setdefault("args", proposal.arguments)
        return context
