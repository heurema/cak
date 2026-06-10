# 01 — Pain Map

CAK should be designed pain-first, not architecture-first.

Pain claims should be backed by sources, interviews, incidents, or marked
assumptions. The initial P0 evidence ledger is
[`evidence/p0_pain_sources.md`](../evidence/p0_pain_sources.md).

## P0 pains

### 1. Agent behavior is not governable

Teams cannot reliably answer:

- Why did the agent do this?
- Which memory was used?
- Which skill fired?
- Which policy allowed the action?
- Who approved it?
- What changed after the last release?
- How do we roll back bad behavior?

**CAK response:** CAK IR, EvidenceSpec, ArtifactRegistry, ArtifactGraph, VerifierReport, AuditLedger, Incident/Unlearning.

**Evidence status:** partially supported by AI risk-management and GenAI trace
standardization sources; still needs direct user interviews and incident traces.

### 2. Agents repeat mistakes instead of learning safely

Agents often fail, then fail the same way again. Worse, they may learn the wrong lesson.

**CAK response:** TraceStore, MemoryCompiler, EffectCompiler, SkillCompiler, EvidenceSpec, Replay, ShadowEval, FailureNonRepetition metric.

**Evidence status:** research-supported, but production pain is not yet proven.

### 3. Unsafe external actions

Agents increasingly get write tools: email, CRM, GitHub, deployments, billing systems, databases, browsers, and OS actions.

**CAK response:** Agency type system, capability/effect calculus, `Action<irreversible>`, `Env<live>`, `Approval<Token>`, Transaction/Saga, Verifier stack, Policy-as-code.

**Evidence status:** partially supported by tool-use APIs and prompt-injection
risk; still needs concrete external-action incidents.

### 4. Cost is unpredictable

Agent cost comes from:

- long context;
- retries;
- pass^k sampling;
- tool calls;
- web/search grounding;
- code execution;
- shadow eval;
- frontier model escalation;
- human review.

**CAK response:** TaskCapsule, CostGuard, FrontierGate, ContextCachePlan, BatchModelPass, ProviderProfile, Cost-per-Gain, FrontierROIReport.

**Evidence status:** weak until measured against real agent traces.

### 5. Vendor lock-in

Lock-in is not only API syntax. It comes from native skills, hidden tool semantics, memory tools, caching behavior, provider fallback semantics, retention policies, and model quirks.

**CAK response:** CAK IR as canonical object format, ProviderProfile, NativeBinding, FallbackGraph, FeatureParityTest, DataRoutingPolicy, PortabilityIndex.

**Evidence status:** supported at API-shape level by provider tool-use docs;
semantic portability still needs a benchmark.

## P1 pains

### 6. Data privacy and retention are hard to reason about

Agent traces can contain PII, secrets, internal docs, financial data, customer records, prompts, memory writes, and tool outputs.

**CAK response:** DataPolicySpec, RetentionRule, RedactionSpec, Purpose-bound capabilities, TraceSanitizer, ProviderProfile, DataRoutingPolicy.

### 7. Memory pollution

Memory becomes false, stale, poisoned, duplicated, over-generalized, or unscoped.

**CAK response:** MemoryCompiler, EvidenceSpec, ScopeSpec, ContradictionManager, Tombstone/Retraction, Memory tests, Multi-index retrieval, Quarantine.

### 8. Skill debt

Large skill libraries can degrade behavior through wrong selection, stale routines, unsafe shortcuts, and shadowing.

**CAK response:** SkillSpec, SkillGraph, Selector, Activation predicates, Verifier suite, Skill health metrics, Deprecation/Quarantine, Package signing, Regression tests.

### 9. Debugging agent behavior is miserable

Raw traces are often huge and semantically unclear.

**CAK response:** Replay, ArtifactGraph, SemanticDiff, TraceDebugger, VerifierReport, AgentBlame, BehavioralDiff.

### 10. Model and environment drift

Behavior breaks when model versions, provider policies, API fields, UI layout, business rules, permissions, or data distributions change.

**CAK response:** EnvDiff, ProviderProfileDiff, ArtifactScope, Replay suites, ShadowEval, ContradictionManager, Drift detectors.

### 11. Multi-agent systems fail in non-obvious ways

Free-form swarms suffer from role confusion, consensus traps, hidden assumptions, poor termination, and weak verification.

**CAK response:** EpistemicBlackboard, Claim/Evidence/Objection, Authority types, Role contracts, Termination conditions, Verifier-gated commits.

### 12. Supply-chain and repo-context attacks

Repo configuration, agent instruction files, hooks, MCP configs, editor automation, and package scripts are executable attack surfaces.

**CAK response:** TrustInspector, RepoIntakeScanner, ContextFirewall, ToolConfigPolicy, Secret scanner, Capability manifest, Compiler-generated context pack.

## P2 pains

### 13. Human approval fatigue

If every risky action asks for approval, humans rubber-stamp.

**CAK response:** Risk-tiered approvals, Proof levels L0-L5, scoped approval tokens, approval batching, policy-derived auto-approval for low-risk reversible actions.

### 14. Organizational ownership gap

When an agent fails, ownership is unclear: model provider, app team, policy owner, skill author, human approver, or tool provider?

**CAK response:** OrgSpec, Artifact ownership, Approval chains, Incident commander, Verifier owner, Domain steward, Audit ledger.

### 15. Eval debt

Teams deploy agents without evaluation culture. Evals arrive late and do not cover real failures.

**CAK response:** EvalSpec, Replay-derived evals, Incident-derived evals, CARE-Bench, Promotion requires eval coverage.

### 16. Artifact entropy

Thousands of memories, skills, effects, policies, provider profiles, env specs, verifiers, evals, patches, and incidents will accumulate.

**CAK response:** ArtifactRegistry, ArtifactGraph, Health metrics, Garbage collection, Deprecation, Tombstones, Compatibility matrix.
