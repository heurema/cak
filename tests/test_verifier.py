import json
from pathlib import Path

import pytest

from cak.specs import GatewayConfig, load_config_file
from cak.verifier import Proposal, verify

CONFIG_PATH = Path(__file__).resolve().parents[1] / "examples" / "v0_1" / "gateway_config.json"


@pytest.fixture()
def config() -> GatewayConfig:
    return load_config_file(CONFIG_PATH)


def _proposal(amount: float, identity: str = "billing-agent") -> Proposal:
    return Proposal(
        identity=identity,
        action="crm.create_invoice",
        arguments={
            "customer_email": "jane@example.com",
            "amount": amount,
            "due_date": "2026-07-01",
        },
    )


def test_allow_with_typed_effect(config: GatewayConfig) -> None:
    decision = verify(config, _proposal(500))
    assert decision.enforcement == "allow"
    assert decision.effect_id == "effect.crm.create_invoice"
    assert decision.risk == "medium"
    assert decision.reversibility == "compensable"
    assert decision.capability_ok


def test_high_amount_requires_approval(config: GatewayConfig) -> None:
    decision = verify(config, _proposal(20000))
    assert decision.enforcement == "require_approval"
    assert "policy.high_amount_requires_approval" in decision.fired_policies


def test_nonpositive_amount_blocked_by_precondition(config: GatewayConfig) -> None:
    decision = verify(config, _proposal(0))
    assert decision.enforcement == "block"
    assert any("precondition failed: amount > 0" in reason for reason in decision.reasons)


def test_strictest_policy_wins() -> None:
    from cak.specs import load_config

    overlapping = load_config(
        {
            "actions": [{"name": "pay", "required_params": ["amount"]}],
            "policies": [
                {"id": "p.warn", "name": "warn", "when": ["amount > 100"],
                 "enforcement": "warn"},
                {"id": "p.approve", "name": "approve", "when": ["amount > 10000"],
                 "enforcement": "require_approval"},
                {"id": "p.block", "name": "block", "when": ["amount > 50000"],
                 "enforcement": "block"},
            ],
            "capabilities": {"billing-agent": ["pay"]},
        }
    )
    decision = verify(overlapping, Proposal("billing-agent", "pay", {"amount": 60000}))
    assert decision.enforcement == "block"
    assert decision.fired_policies == ("p.warn", "p.approve", "p.block")


def test_precondition_failure_blocks(config: GatewayConfig) -> None:
    proposal = Proposal(
        identity="billing-agent",
        action="crm.create_invoice",
        arguments={"customer_email": "x@example.com", "amount": -3, "due_date": None},
    )
    decision = verify(config, proposal)
    assert decision.enforcement == "block"
    assert any("precondition failed" in reason for reason in decision.reasons)


def test_missing_capability_blocks(config: GatewayConfig) -> None:
    decision = verify(config, _proposal(500, identity="unknown-agent"))
    assert decision.enforcement == "block"
    assert not decision.capability_ok


def test_missing_required_params_blocks(config: GatewayConfig) -> None:
    proposal = Proposal("billing-agent", "crm.create_invoice", {"amount": 5})
    decision = verify(config, proposal)
    assert decision.enforcement == "block"
    assert any("missing required params" in reason for reason in decision.reasons)


def test_undeclared_action_blocks(config: GatewayConfig) -> None:
    proposal = Proposal("billing-agent", "crm.delete_everything", {})
    decision = verify(config, proposal)
    assert decision.enforcement == "block"


def test_decision_serializes_to_audit_answer(config: GatewayConfig) -> None:
    decision = verify(config, _proposal(20000))
    payload = json.loads(json.dumps(decision.to_dict()))
    assert payload["enforcement"] == "require_approval"
    assert payload["effect_id"] == "effect.crm.create_invoice"
    assert payload["fired_policies"] == ["policy.high_amount_requires_approval"]
