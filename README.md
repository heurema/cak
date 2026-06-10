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
examples/   Example CAK specs and provider/profile artifacts
```

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
