"""Restricted predicate evaluation for v0.1.

Interim surface until the q-003 language decision (CEL/Cedar/Rego) lands;
see docs/11 "Prefer existing predicate and policy languages". Only two forms
are evaluable:

    <dotted.field> <op> <literal>     op: == != > >= < <=
    <dotted.field>.present

Anything else is UNKNOWN, never a guess (same refusal posture as docs/14:
unevaluable is a first-class result).
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

_COMPARISON = re.compile(
    r"^\s*(?P<field>[A-Za-z_][\w.]*)\s*(?P<op>==|!=|>=|<=|>|<)\s*(?P<value>.+?)\s*$"
)
_PRESENT = re.compile(r"^\s*(?P<field>[A-Za-z_][\w.]*)\.present\s*$")


class Truth(Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


def _resolve(context: dict[str, Any], dotted: str) -> tuple[bool, Any]:
    node: Any = context
    for part in dotted.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return False, None
    return True, node


def _parse_literal(raw: str) -> tuple[bool, Any]:
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        return True, text[1:-1]
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return True, lowered == "true"
    if lowered in {"null", "none"}:
        return True, None
    try:
        return True, int(text)
    except ValueError:
        pass
    try:
        return True, float(text)
    except ValueError:
        return False, None


def evaluate(predicate: str, context: dict[str, Any]) -> Truth:
    """Evaluate one predicate against a context dict. Unevaluable -> UNKNOWN."""
    present = _PRESENT.match(predicate)
    if present:
        found, value = _resolve(context, present.group("field"))
        return Truth.TRUE if found and value is not None else Truth.FALSE

    match = _COMPARISON.match(predicate)
    if not match:
        return Truth.UNKNOWN

    found, actual = _resolve(context, match.group("field"))
    if not found:
        return Truth.UNKNOWN
    ok, expected = _parse_literal(match.group("value"))
    if not ok:
        return Truth.UNKNOWN

    op = match.group("op")
    try:
        if op == "==":
            return Truth.TRUE if actual == expected else Truth.FALSE
        if op == "!=":
            return Truth.TRUE if actual != expected else Truth.FALSE
        if op == ">":
            return Truth.TRUE if actual > expected else Truth.FALSE
        if op == ">=":
            return Truth.TRUE if actual >= expected else Truth.FALSE
        if op == "<":
            return Truth.TRUE if actual < expected else Truth.FALSE
        return Truth.TRUE if actual <= expected else Truth.FALSE
    except TypeError:
        return Truth.UNKNOWN


def evaluate_all(predicates: list[str], context: dict[str, Any]) -> dict[str, Truth]:
    return {predicate: evaluate(predicate, context) for predicate in predicates}
