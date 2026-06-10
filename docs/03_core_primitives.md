# 03 — Core Primitives

The full language should eventually treat these as first-class primitives.

## Minimal core

```text
Trace
Evidence
Effect
Skill
Policy
Capability
Transaction
Memory
Patch
Verifier
Replay
ArtifactRegistry
```

## Full primitive set

```text
Agent
Intent
Goal
Env
Entity
StateSlice
StateDiff
Observation
ActionProposal
ToolContract
Capability
Effect
Invariant
Exception
SideEffect
Reversibility
Risk
Trace
Evidence
Counterexample
Scope
Confidence
MemoryRecord
Skill
Option
Intervention
Verifier
Policy
TemporalRule
Transaction
Approval
Delegation
Protocol
Claim
Objection
Authority
Decision
Patch
EvolutionTransaction
Replay
ShadowEval
EvalSuite
Artifact
Package
Dependency
Incident
Quarantine
Retraction
Budget
DataPolicy
ProviderProfile
TaskCapsule
CostGuard
FallbackGraph
AuditLog
```

## Important distinction

- `Trace` is raw history.
- `Evidence` is selected support/counter-support.
- `Effect` is a guarded action-effect hypothesis.
- `Memory` is compiled state-conditioned knowledge.
- `Skill` is reusable executable behavior with tests and scope.
- `Policy` is a machine-checkable rule.
- `Patch` is a governed mutation of agent behavior.
- `Replay` is a testable reconstruction.
- `ArtifactRegistry` is the package manager for behavior.
