# 08 — Provider, Cost, and Portability

## Principle

Provider-native features are acceleration targets, not canonical semantics.

```text
CAK IR = source of truth
NativeBinding = provider-specific lowering
Provider trace = normalized back into CAK IR
```

## Provider lock-in vectors

| Vector | Example | CAK mitigation |
|---|---|---|
| API shape | Responses vs Messages vs GenerateContent | CAK IR + provider adapters |
| Tool semantics | Provider-native tools behave differently | ActionSpec + EffectSpec |
| Reasoning controls | effort / thinking budget / adaptive thinking | ProviderCapabilityRegistry |
| Structured output | Different JSON schema subsets | Canonical schema subset + conformance tests |
| Caching | automatic vs explicit TTL caches | ContextCachePlan |
| Privacy | retention / ZDR / region differences | DataRoutingPolicy |
| Version churn | preview/snapshot/deprecated models | Pinned ProviderProfile + replay |
| Prompt quirks | hidden behavior coupling | FeatureParityTest |

## Required artifacts

```text
ModelProfile
ProviderCapability
NativeBinding
ProviderAdapter
FallbackGraph
DataRetentionRule
DataRoutingPolicy
ProviderPolicyEvent
CapabilityNegotiationReport
NativeExportArtifact
FeatureParityTest
ProviderEvalResult
TaskCapsule
ModelPass
CostGuard
FrontierGate
PreparedContextPack
ContextCachePlan
BatchModelPass
FrontierROIReport
```

## TaskCapsule

Expensive frontier models should receive compiled tasks, not raw tasks.

```yaml
task_capsule:
  goal: "Design verifier-governed skill promotion policy"
  constraints:
    - preserve_cak_ir_as_canonical
    - no_vendor_locked_solution
    - output_must_be_portable
  output_schema: VerifierPolicyDesign
  budget:
    max_usd: 3.00
    max_frontier_calls: 1
  data_policy:
    allow_external_model: false
```

## Frontier Gate

```yaml
frontier_gate:
  allow_if:
    - task.complexity >= high
    - expected_reuse_value >= high
    - verifier_can_check_output == true
    - output_artifact in [SkillSpec, PolicySpec, VerifierSpec, CAK IRPatch]
  deny_if:
    - output_not_reusable
    - no_structured_output_schema
    - no_eval_available
    - data_policy.provider_conflict == true
```

## Economic metric

```text
Cost per verified reusable behavior
```

not just cost per task.
