# 02 — Full-Solution Architecture

## Architecture summary

CAK should be implemented as a compiler-oriented stack:

```text
CAK surface
  ↓
Parser / Resolver / Typechecker
  ↓
CAK IR canonical artifacts
  ↓
Static analyzer
  ↓
TaskCapsule compiler
  ↓
Agent VM + Provider/Frontier layer + Sandbox/SimSpec
  ↓
Execution Trace Store
  ↓
Memory / Effect / Skill compilers
  ↓
Artifact Registry + ArtifactGraph
  ↓
Verifier stack + Promotion queue
  ↓
Patch / Evolution / Incident / Unlearning
  ↓
Replay / Shadow Eval / CARE-Bench
```

## Layer map

| Layer | Responsibility |
|---|---|
| Surface language | Human-readable CAK in YAML/JSON + Python/TS SDKs |
| CAK IR | Canonical typed IR for agent behavior artifacts |
| Static analyzer | Type checking, policy coverage, scope checks, dependency linting |
| TaskCapsule compiler | Packages execution unit with goal, env, policies, provider and budgets |
| Agent VM | Guarded execution: proposals, verification, transactions, audit |
| Provider layer | Model profiles, native bindings, fallback graphs, cost and data routing |
| Learning compilers | Trace → Memory / Effect / Skill / Patch candidates |
| Verifier stack | Static, pre-exec, post-exec, learning, replay, security, temporal checks |
| Artifact registry | Signed, versioned storage of memories, effects, skills, policies, evals |
| Governance plane | Approvals, review queues, trust tiers, incidents, unlearning |
| Replay/eval plane | Deterministic replay, shadow eval, benchmark scoring, regression suites |
| Devtools | CLI, LSP, semantic diff, trace debugger, trust inspector |
| Ecosystem | Domain packs, standard library, adapters, package manager |

## Design principle

CAK should sit:

- **above protocols** such as MCP and A2A;
- **beside runtimes** such as LangGraph, OpenAI Agents SDK, and Pydantic AI;
- **below application logic** as a semantic execution and learning substrate.

## v0.1 architecture cut

The first product slice should not implement the whole stack.

```text
Existing agent runtime
  -> CAK proposal gateway
  -> effect/capability verifier
  -> policy engine
  -> credential-owning tool gateway
  -> external tool
  -> trace recorder
```

This cut proves whether teams accept CAK at the tool boundary. Learning
compilers, Artifact Registry, provider portability, multi-agent semantics, and
organization-scale governance remain vision-stage until this cut works.

## Runtime flow

```text
Goal
  → TaskCapsule
  → Planner proposes action
  → Verifier checks capabilities/effects/policies
  → Transaction manager preflights/simulates
  → Runtime executes or asks for approval
  → Trace is recorded
  → Postconditions are checked
  → Learning compilers propose artifacts
  → Promotion verifier accepts/rejects/quarantines
  → Replay suite validates behavior
  → Artifact registry updates trusted behavior
```

In v0.1, the runtime flow stops at checked execution and trace recording.
