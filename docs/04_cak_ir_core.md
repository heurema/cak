# 04 — CAK IR Core

CAK IR is the canonical Agent Learning IR.

## Requirements

CAK IR must be:

- typed;
- immutable;
- versioned;
- backend-neutral;
- replayable;
- auditable;
- hashable;
- diffable;
- signable.

## CAK IR node families

| Node | Purpose |
|---|---|
| `GoalSpec` | Target state, constraints, and success tests |
| `EnvSpec` | Environment semantics, entities, actions, hazards |
| `ActionSpec` | Tool/API/UI/A2A action signature |
| `EffectSpec` | Preconditions, effects, exceptions, confidence, evidence |
| `SkillSpec` | Executable behavior contract |
| `MemoryRecord` | Scoped, evidence-backed learned memory |
| `PolicySpec` | Runtime enforcement rule |
| `TransactionSpec` | Saga/checkpoint/compensation model |
| `EvidenceSpec` | Trace-based proof-of-experience |
| `ScopeSpec` | Applicability boundary |
| `VerifierPlan` | Required checks and proof level |
| `ReplaySpec` | Deterministic or shadow rerun plan |
| `EvalSpec` | Evaluation and regression cases |
| `ProviderProfile` | Model/provider capabilities and constraints |
| `TaskCapsule` | Portable unit of agent execution |
| `IncidentReport` | Structured incident and unlearning trigger |

## Type lattice

Examples:

```text
Action<read>
Action<write>
Action<delete>
Action<external_send>
Action<payment>
Action<self_modify>

Tool<read_only>
Tool<write>
Tool<network>
Tool<code_exec>

Env<sandbox>
Env<staging>
Env<live>

Skill<candidate>
Skill<verified>
Skill<approved>
Skill<quarantined>

Memory<unverified>
Memory<verified>
Memory<stale>
Memory<private>
Memory<regulated>

Effect<reversible>
Effect<compensable>
Effect<irreversible>

Cap<Read, Email>
Cap<Write, Invoice.status>
Cap<Send, ExternalEmail>
Cap<SelfModify, Skill>
```

## Core rule

```text
Unsafe agency should fail type-checking before execution.
```
