"""Typed gateway configuration: actions, effects, policies, capabilities.

Field names follow schemas/*.schema.json and examples/invoice_agent.cak.yaml.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .cel import CELError
from .cel import compile_expr as compile_cel

RISK_LEVELS = ("low", "medium", "high", "critical")
REVERSIBILITY = ("reversible", "compensable", "irreversible")
ENFORCEMENTS = ("allow", "warn", "block", "require_approval", "sandbox_only", "quarantine")


class ConfigError(ValueError):
    """Raised when gateway configuration is structurally invalid."""


@dataclass(frozen=True, slots=True)
class ActionSpec:
    name: str
    required_params: tuple[str, ...] = ()
    effect: str | None = None


@dataclass(frozen=True, slots=True)
class CompensationSpec:
    """How to undo a compensable effect with another governed action.

    Argument values are derived, not free-typed: dotted paths into the
    original tool result (`args_from_result`) or into the original call
    arguments (`args_from_args`).
    """

    action: str
    args_from_result: dict[str, str] = field(default_factory=dict)
    args_from_args: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EffectSpec:
    id: str
    action: str
    preconditions: tuple[str, ...]
    causes: tuple[str, ...]
    may_cause: tuple[str, ...]
    risk: str
    reversibility: str
    compensation: CompensationSpec | None = None


@dataclass(frozen=True, slots=True)
class PolicySpec:
    id: str
    name: str
    when: tuple[str, ...]
    enforcement: str
    proof_level: str | None = None
    # Optional action scope: empty = global; entries are exact action names
    # or "prefix.*" globs (same matching as capabilities).
    actions: tuple[str, ...] = ()
    # CEL predicate (docs/11 verdict). When set, it is evaluated instead of
    # the interim `when` list. Exactly one of `when` / `expr` carries the
    # condition; an empty `when` with no `expr` fires unconditionally.
    expr: str | None = None

    def applies_to(self, action: str) -> bool:
        if not self.actions:
            return True
        return any(
            entry == action or (entry.endswith(".*") and action.startswith(entry[:-1]))
            for entry in self.actions
        )


@dataclass(frozen=True, slots=True)
class GatewayConfig:
    actions: dict[str, ActionSpec]
    effects_by_action: dict[str, EffectSpec]
    policies: tuple[PolicySpec, ...]
    capabilities: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def allowed(self, identity: str, action: str) -> bool:
        grants = self.capabilities.get(identity, ())
        return any(
            grant == action or (grant.endswith(".*") and action.startswith(grant[:-1]))
            for grant in grants
        )


def _require(obj: dict[str, Any], key: str, label: str) -> Any:
    if key not in obj:
        raise ConfigError(f"{label}: missing required field '{key}'")
    return obj[key]


def _str_tuple(value: Any, label: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ConfigError(f"{label}: expected a list of strings")
    return tuple(value)


def load_config(data: dict[str, Any]) -> GatewayConfig:
    actions: dict[str, ActionSpec] = {}
    for raw in data.get("actions", []):
        name = str(_require(raw, "name", "action"))
        actions[name] = ActionSpec(
            name=name,
            required_params=_str_tuple(raw.get("required_params"), f"action {name}"),
            effect=raw.get("effect"),
        )

    effects: dict[str, EffectSpec] = {}
    for raw in data.get("effects", []):
        effect_id = str(_require(raw, "id", "effect"))
        action = str(_require(raw, "action", f"effect {effect_id}"))
        risk = str(_require(raw, "risk", f"effect {effect_id}"))
        reversibility = str(_require(raw, "reversibility", f"effect {effect_id}"))
        if risk not in RISK_LEVELS:
            raise ConfigError(f"effect {effect_id}: unknown risk '{risk}'")
        if reversibility not in REVERSIBILITY:
            raise ConfigError(f"effect {effect_id}: unknown reversibility '{reversibility}'")
        compensation: CompensationSpec | None = None
        raw_compensation = raw.get("compensation")
        if raw_compensation is not None:
            if not isinstance(raw_compensation, dict):
                raise ConfigError(f"effect {effect_id}: compensation must be an object")
            compensation = CompensationSpec(
                action=str(_require(raw_compensation, "action", f"effect {effect_id}")),
                args_from_result={
                    str(k): str(v)
                    for k, v in (raw_compensation.get("args_from_result") or {}).items()
                },
                args_from_args={
                    str(k): str(v)
                    for k, v in (raw_compensation.get("args_from_args") or {}).items()
                },
            )
        effects[action] = EffectSpec(
            id=effect_id,
            action=action,
            preconditions=_str_tuple(raw.get("preconditions"), f"effect {effect_id}"),
            causes=_str_tuple(raw.get("causes"), f"effect {effect_id}"),
            may_cause=_str_tuple(raw.get("may_cause"), f"effect {effect_id}"),
            risk=risk,
            reversibility=reversibility,
            compensation=compensation,
        )

    policies: list[PolicySpec] = []
    for raw in data.get("policies", []):
        policy_id = str(_require(raw, "id", "policy"))
        enforcement = str(_require(raw, "enforcement", f"policy {policy_id}"))
        if enforcement not in ENFORCEMENTS:
            raise ConfigError(f"policy {policy_id}: unknown enforcement '{enforcement}'")
        expr = raw.get("expr")
        if expr is not None:
            if "when" in raw:
                raise ConfigError(
                    f"policy {policy_id}: set either 'expr' (CEL) or 'when' (interim), "
                    "not both"
                )
            if not isinstance(expr, str):
                raise ConfigError(f"policy {policy_id}: 'expr' must be a string")
            try:
                compile_cel(expr)
            except CELError as error:
                raise ConfigError(f"policy {policy_id}: {error}") from error
        policies.append(
            PolicySpec(
                id=policy_id,
                name=str(raw.get("name", policy_id)),
                when=_str_tuple(raw.get("when"), policy_id),
                enforcement=enforcement,
                proof_level=raw.get("proof_level"),
                actions=_str_tuple(raw.get("actions"), f"policy {policy_id}"),
                expr=expr,
            )
        )

    capabilities = {
        str(identity): _str_tuple(grants, f"capabilities[{identity}]")
        for identity, grants in data.get("capabilities", {}).items()
    }

    return GatewayConfig(
        actions=actions,
        effects_by_action=effects,
        policies=tuple(policies),
        capabilities=capabilities,
    )


def load_config_file(path: Path) -> GatewayConfig:
    return load_config(json.loads(path.read_text(encoding="utf-8")))
