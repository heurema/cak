# 09 — Evaluation and Benchmarks

## CARE-Bench

CARE = Causal Adaptation, Replay, and Enforcement.

CAK should not rely only on first-pass success benchmarks. It should evaluate whether an agent can fail, learn safely, replay, and improve without repeating the same failure or violating policy.

## Core benchmark question

```text
Did the agent use its own failed trace to behave better later?
```

## Scenario structure

```text
Scenario Family
├── Attempt 1: cold start
│   ├── unfamiliar UI/API/policy trap
│   └── expected: fail or partial
├── Memory Compilation
│   └── trace → memory/effect/skill candidate
├── Attempt 2: near-repeat
│   └── same lesson, different parameters
└── Attempt 3: drift
    └── changed UI/API/policy
```

## Metrics

| Metric | Meaning |
|---|---|
| FirstAttemptSuccess | First-pass capability |
| SecondAttemptLift | Improvement after bounded learning update |
| FailureNonRepetition | Whether prior failure modes disappear |
| RepeatedMistakeRate | Fraction of previous errors repeated |
| CompletionUnderPolicy | Task success while obeying constraints |
| AdaptationUnderShift | Robustness under UI/API/provider drift |
| NegativeTransferRate | Cases where memory hurts performance |
| ActionOutcomePrediction | Quality of effect/world-model predictions |
| CollateralRespect | Avoids unintended state changes |
| CostPerGain | Marginal cost per score improvement |
| pass^k Reliability | Consistency across repeated runs |
| PromotionPrecision | Promoted artifacts that actually help |
| ReplayFidelity | Replay matches original semantic checkpoints |
| TimeToContainment | Incident response speed |

## Baselines

```text
No memory
Raw transcript
Vector retrieval memory
Textual reflection
Workflow memory
Executable skill library
HASP-style intervention functions
Full CAK with Evidence/Scope/Verifier/Replay
```

## Benchmark warning

If raw transcript or simple vector memory matches CAK on second-attempt lift and drift adaptation, the full architecture is overbuilt and should be simplified.
