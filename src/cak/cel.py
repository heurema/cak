"""CEL evaluation for PolicySpec expressions (docs/11 verdict 2026-06-15).

CEL is adopted for `PolicySpec.expr`; the interim predicate surface
(predicates.py) stays for the deprecated `when` list and for effect
pre/postconditions until those migrate too.

celpy is an optional import: configs that use only `when` run without it.
A config that declares `expr` while celpy is missing fails at load time with
a clear error, never silently.

Evaluation semantics mirror the interim surface: an expression that cannot be
evaluated against the given arguments (missing field, type error) does NOT
fire the policy — unevaluable is never a guess (docs/14).
"""

from __future__ import annotations

from typing import Any

_CELPY: Any | None
try:
    import celpy as _celpy_module
except ImportError:  # pragma: no cover - exercised by environment, not tests
    _CELPY = None
else:
    _CELPY = _celpy_module

CEL_AVAILABLE = _CELPY is not None


class CELError(ValueError):
    """Raised when a CEL expression cannot be compiled."""


_PROGRAM_CACHE: dict[str, Any] = {}


def _require_celpy() -> Any:
    if _CELPY is None:
        raise CELError(
            "policy uses a CEL 'expr' but celpy is not installed "
            "(pip install cel-python)"
        )
    return _CELPY


def compile_expr(expr: str) -> None:
    """Validate a CEL expression at config-load time. Raises CELError."""
    celpy = _require_celpy()
    if expr in _PROGRAM_CACHE:
        return
    env = celpy.Environment()
    try:
        ast = env.compile(expr)
        _PROGRAM_CACHE[expr] = env.program(ast)
    except Exception as error:  # celpy raises CELParseError / tree errors
        raise CELError(f"invalid CEL expression {expr!r}: {error}") from error


def evaluate(expr: str, arguments: dict[str, Any]) -> bool:
    """Evaluate a CEL expression against call arguments. Unevaluable -> False."""
    celpy = _require_celpy()
    if expr not in _PROGRAM_CACHE:
        compile_expr(expr)
    program = _PROGRAM_CACHE[expr]
    activation = {"args": celpy.json_to_cel(arguments)}
    try:
        result = program.evaluate(activation)
    except Exception:
        return False
    return bool(result)
