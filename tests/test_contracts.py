import pytest

from cak.contracts import check_contracts, load_contracts
from cak.specs import ConfigError
from cak.types import TypeAtom, TypedState
from cak.verifier import Proposal


def _proposal() -> Proposal:
    return Proposal(
        identity="billing-agent",
        action="crm.send_invoice",
        arguments={"invoice_id": "inv_001"},
    )


def _contract_pack() -> tuple:
    return load_contracts(
        [
            {
                "id": "contract.live_write_requires_effect_spec",
                "name": "live_write_requires_effect_spec",
                "version": "0.1.0",
                "kind": "ContractSpec",
                "hook": "before_action",
                "priority": 0.9,
                "severity": "hard",
                "match": ["env == \"live\"", "action.kind == \"write\""],
                "requires": ["effect.known == true"],
                "violation": {"type": "UnknownEffectError"},
                "repair": {"handlers": [], "on_repair_failure": "block"},
                "status": "candidate",
            },
            {
                "id": "contract.external_send_requires_exact_fresh_approval",
                "name": "external_send_requires_exact_fresh_approval",
                "version": "0.1.0",
                "kind": "ContractSpec",
                "hook": "before_action",
                "priority": 0.95,
                "severity": "hard",
                "match": ["action.kind == \"external_send\""],
                "requires": [
                    "approval.granted == true",
                    "approval.exact_scope == true",
                    "approval.not_expired == true",
                    "approval.single_use == true",
                ],
                "violation": {
                    "type": "MissingApprovalError",
                    "message": "Exact fresh approval required.",
                },
                "repair": {
                    "handlers": ["skill.request_scoped_approval"],
                    "max_attempts": 1,
                    "on_repair_failure": "block",
                },
                "verify": {
                    "target_type": "Approval<GrantedFresh,ExactScope>",
                    "verifier_plan": "verifier.approval_token_exact_scope_valid",
                },
                "status": "candidate",
            },
        ]
    )


def test_type_atom_lookup() -> None:
    state = TypedState(atoms=(TypeAtom("Approval", "GrantedFresh", "approval_1"),))

    assert state.has_atom("Approval", "GrantedFresh")
    assert state.has_atom("Approval", "GrantedFresh", "approval_1")
    assert not state.has_atom("Approval", "Expired")


def test_nonmatching_contract_does_not_fire() -> None:
    contracts = _contract_pack()
    state = TypedState(facts={"env": "live", "action": {"kind": "read"}})

    decision = check_contracts(state, _proposal(), contracts)

    assert decision.ok
    assert decision.violations == ()


def test_unknown_effect_contract_blocks_live_write_without_effect() -> None:
    contracts = _contract_pack()
    state = TypedState(
        facts={
            "env": "live",
            "action": {"kind": "write"},
            "effect": {"known": False},
        }
    )

    decision = check_contracts(state, _proposal(), contracts)

    assert not decision.ok
    assert decision.hard_blocked
    assert len(decision.violations) == 1
    violation = decision.violations[0]
    assert violation.error_type == "UnknownEffectError"
    assert violation.missing == ("effect.known == true",)


def test_exact_approval_contract_passes_when_all_guarantees_are_present() -> None:
    contracts = _contract_pack()
    state = TypedState(
        facts={
            "action": {"kind": "external_send"},
            "approval": {
                "granted": True,
                "exact_scope": True,
                "not_expired": True,
                "single_use": True,
            },
        }
    )

    decision = check_contracts(state, _proposal(), contracts)

    assert decision.ok
    assert decision.violations == ()


def test_unknown_required_guarantees_are_violations() -> None:
    contracts = _contract_pack()
    state = TypedState(facts={"action": {"kind": "external_send"}})

    decision = check_contracts(state, _proposal(), contracts)

    assert not decision.ok
    violation = decision.violations[0]
    assert violation.error_type == "MissingApprovalError"
    assert violation.repair_handlers == ("skill.request_scoped_approval",)
    assert "approval.exact_scope == true" in violation.unknown


def test_violations_are_sorted_by_priority() -> None:
    contracts = _contract_pack()
    state = TypedState(
        facts={
            "env": "live",
            "action": {"kind": "external_send"},
            "effect": {"known": False},
        }
    )

    decision = check_contracts(state, _proposal(), contracts)

    assert [violation.error_type for violation in decision.violations] == [
        "MissingApprovalError",
    ]


def test_loader_rejects_wrong_kind() -> None:
    with pytest.raises(ConfigError, match="unsupported kind"):
        load_contracts(
            [
                {
                    "id": "contract.bad",
                    "name": "bad",
                    "version": "0.1.0",
                    "kind": "SkillSpec",
                    "hook": "before_action",
                    "severity": "hard",
                    "match": [],
                    "requires": [],
                    "violation": {"type": "BadError"},
                    "status": "candidate",
                }
            ]
        )


def test_loader_rejects_unknown_severity() -> None:
    with pytest.raises(ConfigError, match="unknown severity"):
        load_contracts(
            [
                {
                    "id": "contract.bad",
                    "name": "bad",
                    "version": "0.1.0",
                    "kind": "ContractSpec",
                    "hook": "before_action",
                    "severity": "fatal",
                    "match": [],
                    "requires": [],
                    "violation": {"type": "BadError"},
                    "status": "candidate",
                }
            ]
        )
