"""Event-sourced trace: proposals, decisions, outcomes, postconditions.

One JSONL file per gateway session. Events carry a monotonically increasing
sequence number; replay (replay.py) treats the file as the source of truth.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TraceRecorder:
    path: Path
    _seq: int = 0

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            return
        for event in read_trace(self.path):
            seq = event.get("seq")
            if isinstance(seq, int):
                self._seq = max(self._seq, seq)

    def emit(self, event_type: str, payload: dict[str, Any]) -> int:
        self._seq += 1
        record = {"seq": self._seq, "ts": time.time(), "type": event_type, **payload}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return self._seq

    def proposal(self, call_id: Any, identity: str, action: str,
                 arguments: dict[str, Any]) -> int:
        return self.emit(
            "proposal",
            {"call_id": call_id, "identity": identity, "action": action,
             "arguments": arguments},
        )

    def decision(self, call_id: Any, decision: dict[str, Any]) -> int:
        return self.emit("decision", {"call_id": call_id, "decision": decision})

    def outcome(self, call_id: Any, result: dict[str, Any] | None,
                error: dict[str, Any] | None) -> int:
        return self.emit("outcome", {"call_id": call_id, "result": result, "error": error})

    def postconditions(self, call_id: Any, effect_id: str | None,
                       checks: dict[str, str],
                       result_context: dict[str, Any] | None) -> int:
        return self.emit(
            "postconditions",
            {"call_id": call_id, "effect_id": effect_id, "checks": checks,
             "result_context": result_context},
        )


def read_trace(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events
