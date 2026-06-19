"""ContractSpec checker for typed agent-state transitions.

ContractSpec is deliberately separate from SkillSpec: a contract detects an
illegal transition and routes to repair skills; a SkillSpec performs executable
repair work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .predicates import Truth, evaluate_all
from .specs import ConfigError
from .types import TypedState
from .verifier import Proposal

CONTRACT_SEVERITIES = ("hard", "soft", "audit")
CONTRACT_STATUSES = (
    "draft",
    "candidate",
    "shadow_tested",
    "verified",
    "approved",
    "active",
    "deprecated",
    "quarantined",
    "archived",
)


@dataclass(frozen=True, slots=True)
class ViolationSpec:
    type: str
    message: str | None = None


@dataclass(frozen=True, slots=True)
class RepairSpec:
    handlers: tuple[str, ...] = ()
    on_repair_failure: str = "block"
    max_attempts: int = 0


@dataclass(frozen=True, slots=True)
class VerifySpec:
    target_type: str | None = None
    verifier_plan: str | None = None


@dataclass(frozen=True, slots=True)
class ContractSpec:
    id: str
    name: str
    version: str
    hook: str
    severity: str
    match: tuple[str, ...]
    requires: tuple[str, ...]
    violation: ViolationSpec
    status: str
    repair: RepairSpec = field(default_factory=RepairSpec)
    verify: VerifySpec = field(default_factory=VerifySpec)
    priority: float | None = None

    def applies(self, context: dict[str, Any]) -> bool:
        """Return True only when all match predicates are definitely true."""
        if not self.match:
            return True
        results = evaluate_all(list(self.match), context)
        return all(truth is Truth.TRUE for truth in results.values())


@dataclass(frozen=True, slots=True)
class ContractViolation:
    contract_id: str
    error_type: str
    severity: str
    missing: tuple[str, ...]
    unknown: tuple[str, ...]
    repair_handlers: tuple[str, ...]
    message: str | None = None


@dataclass(frozen=True, slots=True)
class ContractDecision:
    ok: bool
    violations: tuple[ContractViolation, ...]

    @property
    def hard_blocked(self) -> bool:
        return any(violation.severity == "hard" for violation in self.violations)


def _require(raw: dict[str, Any], key: str, label: str) -> Any:
    if key not in raw:
        raise ConfigError(f"{label}: missing required field '{key}'")
    return raw[key]


def _str_tuple(value: Any, label: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ConfigError(f"{label}: expected a list of strings")
    return tuple(value)


def _load_violation(raw: Any, label: str) -> ViolationSpec:
    if not isinstance(raw, dict):
        raise ConfigError(f"{label}: violation must be an object")
    return ViolationSpec(
        type=str(_require(raw, "type", label)),
        message=str(raw["message"]) if raw.get("message") is not None else None,
    )


def _load_repair(raw: Any, label: str) -> RepairSpec:
    if raw is None:
        return RepairSpec()
    if not isinstance(raw, dict):
        raise ConfigError(f"{label}: repair must be an object")
    max_attempts = raw.get("max_attempts", 0)
    if not isinstance(max_attempts, int) or max_attempts < 0:
        raise ConfigError(f"{label}: repair.max_attempts must be a non-negative integer")
    return RepairSpec(
        handlers=_str_tuple(raw.get("handlers"), f"{label}.repair.handlers"),
        on_repair_failure=str(raw.get("on_repair_failure", "block")),
        max_attempts=max_attempts,
    )


def _load_verify(raw: Any, label: str) -> VerifySpec:
    if raw is None:
        return VerifySpec()
    if not isinstance(raw, dict):
        raise ConfigError(f"{label}: verify must be an object")
    return VerifySpec(
        target_type=str(raw["target_type"]) if raw.get("target_type") is not None else None,
        verifier_plan=str(raw["verifier_plan"]) if raw.get("verifier_plan") is not None else None,
    )


def load_contracts(data: list[dict[str, Any]]) -> tuple[ContractSpec, ...]:
    contracts: list[ContractSpec] = []
    for raw in data:
        contract_id = str(_require(raw, "id", "contract"))
        kind = str(_require(raw, "kind", f"contract {contract_id}"))
        if kind != "ContractSpec":
            raise ConfigError(f"contract {contract_id}: unsupported kind '{kind}'")
        severity = str(_require(raw, "severity", f"contract {contract_id}"))
        if severity not in CONTRACT_SEVERITIES:
            raise ConfigError(f"contract {contract_id}: unknown severity '{severity}'")
        status = str(_require(raw, "status", f"contract {contract_id}"))
        if status not in CONTRACT_STATUSES:
            raise ConfigError(f"contract {contract_id}: unknown status '{status}'")
        priority = raw.get("priority")
        if priority is not None and not isinstance(priority, (int, float)):
            raise ConfigError(f"contract {contract_id}: priority must be numeric")
        contracts.append(
            ContractSpec(
                id=contract_id,
                name=str(_require(raw, "name", f"contract {contract_id}")),
                version=str(_require(raw, "version", f"contract {contract_id}")),
                hook=str(_require(raw, "hook", f"contract {contract_id}")),
                severity=severity,
                match=_str_tuple(_require(raw, "match", f"contract {contract_id}"), contract_id),
                requires=_str_tuple(
                    _require(raw, "requires", f"contract {contract_id}"), contract_id
                ),
                violation=_load_violation(
                    _require(raw, "violation", f"contract {contract_id}"),
                    f"contract {contract_id}",
                ),
                repair=_load_repair(raw.get("repair"), f"contract {contract_id}"),
                verify=_load_verify(raw.get("verify"), f"contract {contract_id}"),
                priority=float(priority) if priority is not None else None,
                status=status,
            )
        )
    return tuple(contracts)


def check_contracts(
    typed_state: TypedState,
    proposal: Proposal,
    contracts: tuple[ContractSpec, ...],
) -> ContractDecision:
    """Evaluate contracts against the proposed transition.

    `match` predicates decide applicability and must all be TRUE. `requires`
    predicates are stricter: FALSE and UNKNOWN both violate the contract because
    a missing or ungrounded required guarantee is not safe to assume.
    """
    context = typed_state.to_context(proposal)
    violations: list[ContractViolation] = []

    for contract in sorted(
        contracts,
        key=lambda item: item.priority if item.priority is not None else 0.0,
        reverse=True,
    ):
        if not contract.applies(context):
            continue
        results = evaluate_all(list(contract.requires), context)
        failed = tuple(predicate for predicate, truth in results.items() if truth is Truth.FALSE)
        unknown = tuple(predicate for predicate, truth in results.items() if truth is Truth.UNKNOWN)
        if failed or unknown:
            violations.append(
                ContractViolation(
                    contract_id=contract.id,
                    error_type=contract.violation.type,
                    severity=contract.severity,
                    missing=failed + unknown,
                    unknown=unknown,
                    repair_handlers=contract.repair.handlers,
                    message=contract.violation.message,
                )
            )

    return ContractDecision(ok=not violations, violations=tuple(violations))
