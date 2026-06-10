# 06 — Artifact Lifecycle

## Core lifecycle

```text
Draft
  → Candidate
  → ShadowTested
  → Verified
  → Approved
  → Active
  → Patched
  → Deprecated / Quarantined / Archived
```

## Learning pipeline

This is vision-stage, not v0.1 scope.

```text
raw trace
  → episode
  → outcome label
  → candidate memory
  → contrastive rule
  → causal hypothesis
  → skill candidate
  → tests
  → promotion / demotion
```

## Artifact classes

| Artifact | Promotion condition |
|---|---|
| MemoryRecord | Evidence, scope, no unresolved contradictions, retrieval value |
| EffectSpec | Support traces, counterexample handling, confidence threshold |
| SkillSpec | Tests, rollback, scope, no policy violations, shadow eval |
| PolicySpec | Review, coverage, semantic fidelity, no hidden weakening |
| Patch | Replay uplift, regression budget, canary, rollback |
| ProviderProfile | Verified docs/source, parity tests, data policy review |

## EvidenceSpec

Every learned artifact needs proof-of-experience.

```yaml
evidence:
  id: ev_042
  supports: effect.invoice_requires_due_date
  source_traces:
    - trace_001
    - trace_004
  counterexamples:
    - trace_012
  support_count: 2
  counterexample_count: 1
  confidence_model: uncalibrated
  confidence_label: medium
  validity:
    env_scope: [crm_v3]
    expires_on:
      - schema_change
      - policy_change
```

Numeric confidence should not appear until CAK has a documented update rule,
calibration method, and minimum evidence threshold.

## Unlearning

CAK must support:

```text
quarantine
freeze
retract
rollback
forget
tombstone
invalidate
scope_split
downgrade_confidence
notify
postmortem
```

Memory should usually be **demoted before deleted**:

```text
active → dormant → deprecated → tombstoned
```
