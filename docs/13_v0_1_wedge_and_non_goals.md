# 13 - v0.1 Wedge and Non-Goals

## v0.1 thesis

CAK v0.1 should prove one narrow claim:

```text
Tool-using agents can be governed at the tool boundary with typed effects,
capabilities, policy checks, and explainable traces.
```

v0.1 is not the full CAK vision. It is the smallest useful slice that can
validate whether teams will accept CAK in the critical path of agent execution.

## Target user

The first target user is a team running a coding or operations agent with access
to local files, GitHub, shell commands, or a small set of SaaS APIs.

The first pain is unsafe or unexplained external action:

- Why did the agent try to mutate state?
- Which capability allowed or blocked it?
- Which policy made the decision?
- What actually changed?
- Can the team audit the denial or approval later?

## v0.1 scope

v0.1 should include:

- `ActionSpec` for tool calls crossing the boundary.
- `EffectSpec` with risk and reversibility.
- `PolicySpec` for allow, block, warn, and require-approval decisions.
- Capability manifest for tools and identities.
- Pre-execution verifier.
- Tool gateway that owns credentials and dispatches allowed calls.
- Trace recorder for proposals, decisions, tool calls, and outcomes.
- Minimal replay using recorded tool calls and semantic checkpoints.
- Example integration with one existing agent stack.

## Adoption ladder

CAK should support gradual adoption:

```text
Level 0: Trace only
Level 1: Tool boundary checks
Level 2: Recorded tool-call replay
Level 3: Evidence-backed effect and memory candidates
Level 4: Verified learning artifacts and unlearning
```

Teams should not need to adopt learning, registry, provider portability, or
multi-agent features to get value from Level 1.

## Explicit non-goals for v0.1

v0.1 should not include:

- automatic trace-to-skill learning;
- generalized memory promotion;
- multi-agent blackboards or claim/objection systems;
- marketplace or package manager;
- provider portability across all frontier models;
- formal proof levels above simple runtime checks;
- visual builders;
- custom general-purpose programming language;
- full enterprise governance role model;
- complete cost-optimization plane.

## What remains vision-stage

These are part of the CAK vision, but should not block v0.1:

- Artifact Registry and ArtifactGraph.
- Evidence-backed promotion of memory, effects, skills, and patches.
- Provenance-driven unlearning.
- Shadow evaluation and full CARE-Bench.
- Provider parity and fallback graphs.
- Organization-scale approval chains and incidents.

## v0.1 success criteria

v0.1 is successful when a real team can instrument one agent and answer:

```text
The agent proposed action X.
CAK classified it as effect Y.
Policy Z allowed or blocked it.
The tool gateway did or did not execute it.
Trace T shows the decision and outcome.
```

## v0.1 kill criteria

Stop or redesign v0.1 if:

- adding CAK requires rewriting the agent architecture;
- a simple agent integration needs more than 300 lines of CAK boilerplate;
- verifier latency adds more than 500 ms per tool action for common cases;
- false blocks affect more than 3% of legitimate production actions;
- teams prefer LangSmith/OpenTelemetry traces plus OPA/Cedar policy with much
  less integration cost;
- traces cannot answer denial and approval questions without manual log digging.

