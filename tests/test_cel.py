"""CEL PolicySpec surface (docs/11 verdict). Skipped when celpy is absent."""

import pytest

pytest.importorskip("celpy")

from cak.cel import CELError, compile_expr
from cak.cel import evaluate as cel_evaluate
from cak.specs import ConfigError, load_config
from cak.verifier import Proposal, verify


def test_compile_rejects_garbage() -> None:
    with pytest.raises(CELError):
        compile_expr("args.amount >>> 3")


def test_evaluate_basic_and_absence() -> None:
    assert cel_evaluate("args.amount > 200", {"amount": 500}) is True
    assert cel_evaluate("args.amount > 200", {"amount": 50}) is False
    assert cel_evaluate("!('reason' in args)", {"amount": 50}) is True
    assert cel_evaluate("!('reason' in args)", {"reason": "x"}) is False


def test_unevaluable_does_not_fire() -> None:
    # Missing field: must not guess (docs/14), so the policy does not fire.
    assert cel_evaluate("args.amount > 200", {"other": 1}) is False


def test_cross_field_and_membership_in_verifier() -> None:
    config = load_config(
        {
            "actions": [
                {"name": "billing.refund_order", "required_params": ["amount"]},
                {"name": "deploy.promote_release", "required_params": ["environment"]},
            ],
            "policies": [
                {
                    "id": "p.refund_exceeds_total",
                    "name": "refund_exceeds_total",
                    "enforcement": "block",
                    "actions": ["billing.refund_order"],
                    "expr": "args.amount > args.order_total",
                },
                {
                    "id": "p.unknown_env",
                    "name": "unknown_env",
                    "enforcement": "block",
                    "actions": ["deploy.promote_release"],
                    "expr": "!(args.environment in ['staging', 'qa', 'production'])",
                },
            ],
            "capabilities": {"agent": ["billing.*", "deploy.*"]},
        }
    )

    over = verify(config, Proposal("agent", "billing.refund_order",
                                   {"amount": 50, "order_total": 30}))
    assert over.enforcement == "block"
    assert over.fired_policies == ("p.refund_exceeds_total",)

    under = verify(config, Proposal("agent", "billing.refund_order",
                                    {"amount": 20, "order_total": 30}))
    assert under.enforcement == "allow"

    bad_env = verify(config, Proposal("agent", "deploy.promote_release",
                                      {"environment": "qa2"}))
    assert bad_env.enforcement == "block"

    ok_env = verify(config, Proposal("agent", "deploy.promote_release",
                                     {"environment": "staging"}))
    assert ok_env.enforcement == "allow"


def test_expr_and_when_are_mutually_exclusive() -> None:
    with pytest.raises(ConfigError, match="not both"):
        load_config(
            {
                "actions": [{"name": "a", "required_params": []}],
                "policies": [
                    {"id": "p", "name": "p", "enforcement": "block",
                     "when": ["x > 1"], "expr": "args.x > 1"}
                ],
                "capabilities": {"agent": ["a"]},
            }
        )


def test_invalid_expr_rejected_at_load() -> None:
    with pytest.raises(ConfigError, match="invalid CEL"):
        load_config(
            {
                "actions": [{"name": "a", "required_params": []}],
                "policies": [
                    {"id": "p", "name": "p", "enforcement": "block",
                     "expr": "args.x >>> 1"}
                ],
                "capabilities": {"agent": ["a"]},
            }
        )
