import json
from pathlib import Path

import pytest

from cak.replay import replay
from cak.specs import GatewayConfig, load_config, load_config_file
from cak.trace import TraceRecorder, read_trace
from cak.verifier import Proposal, verify

CONFIG_PATH = Path(__file__).resolve().parents[1] / "examples" / "v0_1" / "gateway_config.json"


@pytest.fixture()
def config() -> GatewayConfig:
    return load_config_file(CONFIG_PATH)


def _record_session(config: GatewayConfig, path: Path) -> None:
    recorder = TraceRecorder(path)
    arguments = {
        "customer_email": "jane@example.com",
        "amount": 500,
        "due_date": "2026-07-01",
    }
    proposal = Proposal("billing-agent", "crm.create_invoice", arguments)
    decision = verify(config, proposal)
    recorder.proposal(1, proposal.identity, proposal.action, arguments)
    recorder.decision(1, decision.to_dict())
    result_context = {"invoice": {"id": "inv_001", "status": "draft"}}
    recorder.outcome(1, {"structuredContent": result_context}, None)
    recorder.postconditions(
        1,
        decision.effect_id,
        {'invoice.status == "draft"': "true", "invoice.id.present": "true"},
        result_context,
    )


def test_trace_roundtrip(tmp_path: Path, config: GatewayConfig) -> None:
    trace_path = tmp_path / "session.jsonl"
    _record_session(config, trace_path)
    events = read_trace(trace_path)
    assert [event["type"] for event in events] == [
        "proposal", "decision", "outcome", "postconditions",
    ]
    assert [event["seq"] for event in events] == [1, 2, 3, 4]


def test_trace_append_continues_sequence(tmp_path: Path, config: GatewayConfig) -> None:
    trace_path = tmp_path / "session.jsonl"
    _record_session(config, trace_path)
    _record_session(config, trace_path)

    events = read_trace(trace_path)
    assert [event["seq"] for event in events] == list(range(1, 9))


def test_replay_matches_recorded_session(tmp_path: Path, config: GatewayConfig) -> None:
    trace_path = tmp_path / "session.jsonl"
    _record_session(config, trace_path)
    report = replay(config, trace_path)
    assert report.ok
    assert report.proposals == 1
    assert report.decisions_checked == 1
    assert report.postconditions_checked == 1


def test_replay_handles_reused_call_ids_in_appended_sessions(
    tmp_path: Path, config: GatewayConfig
) -> None:
    trace_path = tmp_path / "session.jsonl"
    _record_session(config, trace_path)
    _record_session(config, trace_path)

    report = replay(config, trace_path)
    assert report.ok
    assert report.proposals == 2
    assert report.decisions_checked == 2
    assert report.postconditions_checked == 2


def test_replay_detects_policy_change(tmp_path: Path, config: GatewayConfig) -> None:
    trace_path = tmp_path / "session.jsonl"
    _record_session(config, trace_path)

    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    for policy in raw["policies"]:
        if policy["id"] == "policy.high_amount_requires_approval":
            policy["when"] = ["amount > 100"]
    changed = load_config(raw)

    report = replay(changed, trace_path)
    assert not report.ok
    divergence = report.divergences[0]
    assert divergence.checkpoint == "decision"
    assert divergence.replayed["enforcement"] == "require_approval"


def test_replay_detects_postcondition_drift(tmp_path: Path, config: GatewayConfig) -> None:
    trace_path = tmp_path / "session.jsonl"
    recorder = TraceRecorder(trace_path)
    arguments = {
        "customer_email": "jane@example.com",
        "amount": 500,
        "due_date": "2026-07-01",
    }
    decision = verify(config, Proposal("billing-agent", "crm.create_invoice", arguments))
    recorder.proposal(1, "billing-agent", "crm.create_invoice", arguments)
    recorder.decision(1, decision.to_dict())
    # Recorded checks claim "draft", but the recorded result says "failed":
    # replay must re-evaluate and flag the divergence.
    recorder.postconditions(
        1,
        decision.effect_id,
        {'invoice.status == "draft"': "true", "invoice.id.present": "true"},
        {"invoice": {"id": "inv_001", "status": "failed"}},
    )
    report = replay(config, trace_path)
    assert not report.ok
    assert report.divergences[0].checkpoint == "postconditions"
