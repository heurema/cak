"""exp-005 runner: evaluate the policy corpus in CEL, Rego/OPA, and Cedar.

Usage:  /tmp/exp005-venv/bin/python experiments/predicate-language/run_comparison.py

For each language: run the 15 scenarios, compare the strictest-wins
enforcement against the expected outcome, and measure per-decision latency.
CEL runs in-process (celpy); OPA and Cedar run via their CLIs (subprocess
cost is part of the embedding-cost score until an in-process binding is
adopted).
"""

from __future__ import annotations

import json
import statistics
import subprocess
import time
from pathlib import Path
from typing import Any

import celpy

HERE = Path(__file__).resolve().parent
SEVERITY = {"allow": 0, "warn": 1, "require_approval": 2, "block": 3}
CEDAR = str(Path.home() / ".cargo" / "bin" / "cedar")


def strictest(enforcements: list[str]) -> str:
    decision = "allow"
    for enf in enforcements:
        if SEVERITY[enf] > SEVERITY[decision]:
            decision = enf
    return decision


def percentile(samples: list[float], pct: float) -> float:
    ordered = sorted(samples)
    index = min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1)))
    return ordered[index]


# -- CEL ---------------------------------------------------------------------


def build_cel() -> list[dict[str, Any]]:
    env = celpy.Environment()
    compiled = []
    for policy in json.loads((HERE / "cel_policies.json").read_text())["policies"]:
        program = env.program(env.compile(policy["expr"]))
        compiled.append({**policy, "program": program})
    return compiled


def eval_cel(compiled: list[dict[str, Any]], action: str,
             args: dict[str, Any]) -> str:
    activation = {"args": celpy.json_to_cel(args)}
    fired = []
    for policy in compiled:
        if action not in policy["actions"]:
            continue
        if policy["program"].evaluate(activation):
            fired.append(policy["enforcement"])
    return strictest(fired)


# -- Rego / OPA --------------------------------------------------------------


def eval_rego(action: str, args: dict[str, Any]) -> str:
    request = json.dumps({"action": action, "args": args})
    result = subprocess.run(
        ["opa", "eval", "--format", "json", "--stdin-input",
         "--data", str(HERE / "rego" / "policies.rego"), "data.cak.fired"],
        input=request, capture_output=True, text=True, check=True,
    )
    expressions = json.loads(result.stdout)["result"][0]["expressions"][0]["value"]
    return strictest([item["enf"] for item in expressions])


# -- Cedar -------------------------------------------------------------------

CEDAR_TIERS = [("block", "block.cedar"), ("require_approval", "require_approval.cedar"),
               ("warn", "warn.cedar")]


def eval_cedar(action: str, args: dict[str, Any], workdir: Path) -> str:
    context_path = workdir / "context.json"
    context_path.write_text(json.dumps(args), encoding="utf-8")
    fired = []
    for tier, policy_file in CEDAR_TIERS:
        result = subprocess.run(
            [CEDAR, "authorize",
             "--policies", str(HERE / "cedar" / policy_file),
             "--entities", str(HERE / "cedar" / "entities.json"),
             "--principal", 'User::"support-agent"',
             "--action", f'Action::"{action}"',
             "--resource", 'Gateway::"tools"',
             "--context", str(context_path)],
            capture_output=True, text=True,
        )
        if result.stdout.strip().startswith("ALLOW"):
            fired.append(tier)
    return strictest(fired)


# -- Runner ------------------------------------------------------------------


def main() -> int:
    scenarios = json.loads((HERE / "scenarios.json").read_text())["scenarios"]
    report: dict[str, Any] = {}

    import tempfile
    workdir = Path(tempfile.mkdtemp())

    compiled_cel = build_cel()
    evaluators = {
        "cel": lambda a, g: eval_cel(compiled_cel, a, g),
        "rego_opa_cli": eval_rego,
        "cedar_cli": lambda a, g: eval_cedar(a, g, workdir),
    }

    for name, evaluate in evaluators.items():
        mismatches = []
        for scenario in scenarios:
            got = evaluate(scenario["action"], scenario["args"])
            if got != scenario["expect"]:
                mismatches.append(
                    {"id": scenario["id"], "expect": scenario["expect"], "got": got}
                )

        rounds = 50 if name == "cel" else 2
        samples: list[float] = []
        for _ in range(rounds):
            for scenario in scenarios:
                start = time.perf_counter()
                evaluate(scenario["action"], scenario["args"])
                samples.append((time.perf_counter() - start) * 1000)

        report[name] = {
            "scenarios": len(scenarios),
            "correct": len(scenarios) - len(mismatches),
            "mismatches": mismatches,
            "latency_ms": {
                "p50": round(statistics.median(samples), 3),
                "p99": round(percentile(samples, 99), 3),
                "samples": len(samples),
            },
        }
        print(f"{name}: {report[name]['correct']}/{len(scenarios)} correct, "
              f"p50={report[name]['latency_ms']['p50']}ms "
              f"p99={report[name]['latency_ms']['p99']}ms")

    (HERE / "results.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    ok = all(lang["correct"] == lang["scenarios"] for lang in report.values())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
