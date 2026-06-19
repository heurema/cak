# CAK

**CAK** (**Causal Agent Kernel**) is a typed semantic control layer for AI-agent behavior.

CAK is not a general-purpose programming language, a prompt DSL, or another orchestration framework. It is a three-layer system:

1. **CAK Spec** — a human-facing declarative surface format for agent behavior artifacts.
2. **CAK IR** — the canonical typed Agent Learning IR.
3. **CAK Runtime / Governance / Learning Plane** — execution, verification, replay, promotion, audit, portability, cost control, and unlearning.

## Product thesis

> **CAK makes agent behavior a governed software artifact.**

Modern agents can act, but teams struggle to govern what agents learn, how they change, why they act, how much they cost, and whether behavior remains portable across vendors and runtimes.

CAK treats traces, effects, skills, memory, policies, provider bindings, approvals, and patches as replayable, auditable, portable software artifacts.

## v0.1 wedge

The first usable CAK slice is intentionally narrow:

```text
Tool-using agent
-> structured action proposal
-> effect and capability check
-> policy decision
-> tool gateway execution
-> trace
```

v0.1 should prove tool-boundary governance before attempting automatic learning,
full replay, multi-agent coordination, or provider portability.

The preferred v0.1 form factor is an MCP gateway/proxy for SaaS and operations
agents, because it can govern tool calls without requiring agent rewrites.

## Core loop

```text
Observation
→ Trace
→ Evidence
→ Effect
→ Memory / Skill / Patch
→ Verification
→ Replay / Shadow Eval
→ Promotion
→ Runtime Use
→ Audit / Incident / Unlearning
```

## What CAK addresses

- unsafe external actions;
- opaque agent behavior;
- repeated failures;
- memory pollution;
- skill debt;
- vendor lock-in;
- unpredictable frontier-model cost;
- data routing and retention;
- multi-agent failure modes;
- supply-chain and repo-context attacks;
- debugging, replay, audit, rollback, and unlearning.

## Repository map

```text
docs/       Project thesis, pain map, architecture, runtime, governance, evals
evidence/   Source ledger for pain claims and market assumptions
schemas/    Draft CAK IR, TaskCapsule, EffectSpec, SkillSpec, PolicySpec schemas
examples/   Example CAK specs, provider/profile artifacts, v0.1 demo
src/cak/    v0.1 runtime skeleton: specs, verifier, trace, replay, MCP gateway
tests/      Verifier, trace/replay, and gateway end-to-end tests
```

## v0.1 runtime skeleton

The first executable slice (docs/13 scope, docs/17 positioning): typed specs,
an embeddable pre-execution verifier, a JSONL trace recorder, semantic
replay, and an MCP stdio gateway that owns upstream credentials.

```sh
ruff check src tests && mypy src && pytest
PYTHONPATH=src python3 examples/v0_1/demo.py
```

The demo shows the wedge: auto-allow as `Effect<compensable>` with
postcondition checks, `require_approval` with a scoped single-use approval
token (`python3 -m cak.approve`, see docs/18), `block` as a typed replayable
denial, a verified compensation chain on compensable effects
(`compensation_prepared` → `compensation_executed`, see docs/19), and replay
over the recorded trace with decision and postcondition checkpoints.
Predicates are an interim restricted surface until the policy language
decision in `docs/11`.

To put the gateway in front of any MCP server for a real agent (for example
Claude Code), point the client at the proxy command — see
`examples/v0_1/mcp_config_example.json`. The agent needs zero code changes;
upstream credentials live in the gateway environment.

## Naming

The public project name is **CAK**.

Earlier working names such as **CAK-L**, **TraceLang**, and **TLIR** are now treated as legacy aliases:

- `TraceLang` → **CAK Spec**
- `TLIR` → **CAK IR**
- `CAK-L` → **CAK**

## First repo goal

Document the full solution, then cut it down to a testable v0.1:

```text
v0.1: Agent proposal -> Effect/Capability -> Policy -> Tool Gateway -> Trace
vision: CAK Spec -> CAK IR -> Agent VM -> Evidence/Scope -> Verifier -> Artifact Registry -> Replay/Eval -> Provider/Cost/Governance
```

Start with:

- [v0.1 Wedge and Non-Goals](docs/13_v0_1_wedge_and_non_goals.md)
- [Grounding, Enforcement, and Replay](docs/14_grounding_enforcement_replay.md)
- [Authoring Economics](docs/15_authoring_economics.md)
- [CAK Failure Modes](docs/16_cak_failure_modes.md)

Design notes beyond v0.1:

- [Contract Type-System Skills](docs/20_contract_type_system_skills.md)
