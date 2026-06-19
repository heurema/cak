# 20 — Contract Type-System Skills

Status: design note for implementation planning. This is not v0.1 hot-path scope.

## One-sentence idea

A **Contract Skill** is an executable type constraint over an agent state transition: it declares that a proposed action is illegal unless the current typed state contains the required evidence, entity resolution, approval, effect, or verification guarantees.

```text
LLM proposes.
State typer assigns agent-specific types.
Contract checker validates the proposed transition.
Violations become typed errors.
Repair skills attempt to produce the missing type.
Verifier proves the repaired state before retrying or committing.
```

The core product intuition is:

```text
hallucination          = using Claim<Unverified> as Claim<Supported>
premature finalization = calling FINAL with Answer<Draft>
wrong entity focus     = using Entity<Ambiguous> as Entity<Resolved>
unsafe tool use        = executing Action<ExternalSideEffect> without Approval<GrantedFresh>
untested code          = submitting Code<Generated> where Code<Verified> is required
```

## Why this belongs in CAK

CAK already frames itself as a typed semantic control layer. The existing v0.1 wedge is a tool-boundary verifier:

```text
ActionProposal + EffectSpec + Capability + PolicySpec -> allow/block/approval
```

Contract skills generalize this pattern from external tool effects to broader agent cognition and procedural memory:

```text
TypedState + ProposedAction + ContractSpec -> allow | warn | block | repair | ask | quarantine
```

This should not replace the v0.1 gateway. Instead, it should become the next semantic layer once CAK has working enforcement, trace, and replay.

## Research anchors

This design combines three lines of prior work:

1. **Voyager-style executable skills**: skills are code artifacts that can be executed, verified, stored, retrieved, and composed.
2. **AWM-style workflow memory**: reusable workflows can be induced from prior trajectories, abstracted into subroutines, and reused on future tasks.
3. **HASP-style Program Functions**: skills should not merely be prompt text; they can run inside the agent loop, activate on failure-prone states, and modify actions or inject corrective context.

Contract skills add one more layer:

```text
not just: when state S appears, intervene with skill K
but: action A is type-illegal in state S unless guarantee G is present
```

The runtime therefore retrieves repair skills by **type error**, not only by semantic similarity.

## Existing CAK artifacts this builds on

Current repository fit:

- `docs/03_core_primitives.md` already lists `Claim`, `Evidence`, `Verifier`, `Policy`, `Capability`, `Intervention`, `Protocol`, `Transaction`, `Approval`, `Patch`, and `ArtifactRegistry` as primitives.
- `docs/04_cak_ir_core.md` already defines CAK IR as typed, immutable, versioned, replayable, auditable, and includes `SkillSpec`, `PolicySpec`, `EvidenceSpec`, `VerifierPlan`, `EvalSpec`, and `TaskCapsule` as node families.
- `docs/05_agent_vm_runtime.md` already states the key runtime principle: `LLM proposes. Kernel verifies. Runtime commits.`
- `docs/06_artifact_lifecycle.md` already defines a promotion lifecycle and a learning pipeline from raw trace to causal hypothesis to skill candidate to tests.
- `schemas/skill_spec.schema.json` already has skill kinds for `option`, `intervention`, `workflow`, and `executable_program`, but it does not have a contract surface.
- `src/cak/verifier.py` already implements a pure pre-execution verifier that returns an explainable `Decision` over action, effect, risk, reversibility, capability, fired policies, reasons, and precondition unknowns.

So the new design should be additive:

```text
v0.1: capability/effect/policy verifier at tool boundary
v0.2: contract checker and typed state model
v0.3: contract-driven repair skills and learning compiler
```

## Schema decision: use ContractSpec, not SkillSpec.kind=contract

The examples in this document are **ContractSpec-shaped**, not valid instances of the current `SkillSpec` schema.

This matters because the current `schemas/skill_spec.schema.json` is intentionally strict:

```text
additionalProperties: false
required: id, name, version, trigger, preconditions, steps, postconditions, risk, status
kind: option | intervention | workflow | executable_program
```

A contract needs different first-class fields:

```text
hook
match
applies_when
requires
violation
repair
verify
severity
priority
telemetry
```

Therefore, the v0.2 implementation should not simply add `contract` to `SkillSpec.kind`. That would produce examples that look endorsed but fail schema validation, or it would force contract semantics into misleading `trigger/preconditions/steps/postconditions` slots.

Recommended direction:

```text
Introduce ContractSpec as a sibling artifact.
ContractSpec links to SkillSpec repair handlers.
SkillSpec remains the executable/workflow behavior unit.
PolicySpec remains the authorization/compliance rule unit.
```

Possible files:

```text
schemas/contract_spec.schema.json
src/cak/types.py
src/cak/contracts.py
tests/test_contracts.py
examples/v0_2/contract_specs.yaml
```

Relationship:

```text
ContractSpec:
  detects illegal typed transitions
  emits typed violations
  names repair SkillSpecs
  names VerifierPlans

SkillSpec:
  executes repair workflows, interventions, options, or programs

PolicySpec:
  enforces organizational authorization and compliance decisions
```

A future UI or registry may group contracts under a broader human-facing “skills” category, but the canonical CAK IR should keep `ContractSpec` separate unless a later schema design proves that merging is safe.

## Contract Skill vs existing primitives

| Primitive | Current role | Contract relationship |
|---|---|---|
| `EffectSpec` | Describes external action preconditions, causes, risk, reversibility | Contracts may require a known `EffectSpec` before live execution. |
| `PolicySpec` | Machine-checkable enforcement rule | Contracts can compile into policies for hard enforcement, but also carry repair handlers and verifier plans. |
| `SkillSpec` | Reusable executable behavior with tests and scope | Contracts route violations to repair skills; they should not be encoded as ordinary SkillSpecs in v0.2. |
| `VerifierPlan` | Required checks and proof level | Contracts declare which verifier upgrades the state to the required type. |
| `EvidenceSpec` | Proof-of-experience for learned artifacts | Contracts must cite traces, counterexamples, tests, and replay outcomes before promotion. |
| `ReplaySpec` / `EvalSpec` | Regression and semantic replay | Contracts require positive and negative replay fixtures to avoid overblocking. |

## Core concepts

### 1. Typed state

A typed state is not a full world model. It is the subset of agent state that contracts can evaluate.

Examples:

```text
Task<FactualQA>
Task<CreativeWriting>
Task<SaaSWrite>

Claim<Unverified>
Claim<ExtractedFrom:doc_4>
Claim<Supported>
Claim<Contradicted>
Claim<Stale>

Answer<Draft>
Answer<PartiallySupported>
Answer<Verified>

Entity<Mentioned>
Entity<Candidate>
Entity<Ambiguous>
Entity<Resolved>

EvidenceChain<Missing>
EvidenceChain<Partial>
EvidenceChain<Complete>
EvidenceChain<Conflicting>

Action<ReadOnly>
Action<Write>
Action<ExternalSend>
Action<Financial>
Action<Irreversible>

Approval<Missing>
Approval<Requested>
Approval<GrantedFresh>
Approval<Expired>

Code<Generated>
Code<SyntaxChecked>
Code<Tested>
Code<Verified>
```

Typed state should be gradual. Most runtime facts begin as unknown:

```text
Claim<Unknown> -> Claim<ExtractedFrom> -> Claim<Supported> -> Claim<Verified>
Entity<Unknown> -> Entity<Candidate> -> Entity<Ambiguous|Resolved>
Action<Proposed> -> Action<Allowed|Blocked|NeedsRepair>
```

### 2. Contract

A contract declares the legality of a transition.

```text
match proposed action A
requires typed predicates P
otherwise emit violation E
optionally repair using handler H
verify target type T after repair
```

### 3. Typed violation

A violation is the central routing object.

```text
MissingEvidenceError
AmbiguousEntityError
UnsafeSideEffectError
UnknownEffectError
MissingApprovalError
UntestedCodeError
IncompleteEvidenceChainError
BudgetContractError
```

Instead of retrieving a skill by embedding similarity, CAK can route:

```text
MissingEvidenceError -> acquire_evidence repair workflow
AmbiguousEntityError -> resolve_entity repair workflow
UnsafeSideEffectError -> ask_user_confirmation / simulate / block
UntestedCodeError -> run_tests / generate_edge_cases
```

### 4. Repair skill

A repair skill is an executable or workflow skill that tries to produce the missing type.

Examples:

```text
Answer<Draft> -> acquire_evidence -> Answer<Supported>
Entity<Ambiguous> -> resolve_entity -> Entity<Resolved>
Code<Generated> -> run_tests -> Code<Verified>
Approval<Missing> -> ask_user -> Approval<GrantedFresh>
```

Repair execution must go through the same gateway and policy checks as any other action. A repair skill must never bypass capability, policy, effect, or approval checks.

### 5. Verifier

The verifier is what upgrades a type. The agent should not be allowed to self-assert the upgrade without evidence.

```text
read_count > 0 does not automatically mean Answer<Verified>
source_supports_claim(claim, doc) may produce Claim<Supported>
all_claims_supported(answer) may produce Answer<Verified>
approval_token.valid && approval_token.scope_matches_exact_call may produce Approval<GrantedFresh>
```

## Proposed runtime flow

```text
1. OBSERVE
2. NORMALIZE_STATE
3. INFER_TYPES
4. PROPOSE_ACTION
5. CHECK_CONTRACTS
6. If contracts OK: continue to current v0.1 capability/effect/policy verifier
7. If contract violation:
   a. emit typed violation
   b. route to repair skill
   c. execute repair through the same guarded gateway
   d. verify target type
   e. retry original action, downgrade, ask, or block
8. EXECUTE
9. VERIFY_POSTCONDITIONS
10. WRITE_TRACE
11. REPLAY / SHADOW EVAL
```

The important separation is:

```text
LLM proposal          = what the model wants to do
Contract checker      = whether that transition is legal in typed state
Repair skill          = how to produce the missing guarantee
Verifier              = whether repair actually produced it
v0.1 gateway verifier = whether the external tool call is authorized and effect-safe
```

## Minimal ContractSpec surface format

```yaml
id: contract.final_requires_verified_answer
name: final_requires_verified_answer
version: 0.1.0
kind: ContractSpec
status: candidate

hook: before_action
priority: 0.95
severity: hard

match:
  action: FINAL

applies_when:
  - task.kind in [factual_qa, web_research, legal_research, support_answer]

requires:
  - answer.type == Answer<Verified>
  - evidence_chain.state == EvidenceChain<Complete>
  - answer.claims.all_supported == true

violation:
  type: MissingEvidenceError
  message: FINAL requires verified answer for factual tasks.

repair:
  handlers:
    - skill.acquire_evidence
    - skill.resolve_missing_hop
  max_attempts: 1
  on_repair_failure: block

verify:
  target_type: Answer<Verified>
  verifier_plan: verifier.answer_supported_by_read_evidence

tests:
  positive:
    - trace.final_without_read_factual_001
    - trace.multihop_partial_evidence_004
  negative:
    - trace.creative_writing_no_evidence_001
    - trace.simple_arithmetic_direct_002

scope:
  env: [web_search_agent]
  expires_on: [policy_change, verifier_change]

evidence:
  source_traces:
    - trace.final_without_read_factual_001
  counterexamples:
    - trace.creative_writing_no_evidence_001
  support_count: 1
  counterexample_count: 1
  confidence_model: uncalibrated
  confidence_label: low

telemetry:
  track:
    - activation_count
    - false_positive_rate
    - repair_success_rate
    - downstream_success_delta
    - added_steps
```

## Example: external side-effect approval contract

This is closer to the existing SaaS/ops tool-boundary implementation than factual QA.

The key rule is exact approval scope, not action-class approval. In v0.1, approval is scoped to:

```text
identity + action + sha256(canonical arguments)
```

So a token approved for one recipient, amount, invoice, or payload must never authorize a different call with the same action name.

```yaml
id: contract.external_send_requires_exact_fresh_approval
name: external_send_requires_exact_fresh_approval
version: 0.1.0
kind: ContractSpec
status: candidate

hook: before_action
severity: hard

match:
  action_type: Action<ExternalSend>

requires:
  - approval.type == Approval<GrantedFresh>
  - approval.identity == proposal.identity
  - approval.action == proposal.action
  - approval.args_hash == sha256(canonical(proposal.arguments))
  - approval.not_expired == true
  - approval.single_use == true

violation:
  type: MissingApprovalError

repair:
  handlers:
    - skill.request_scoped_approval
  on_repair_failure: block

verify:
  target_type: Approval<GrantedFresh>
  verifier_plan: verifier.approval_token_exact_scope_valid
```

Compiled to the current v0.1 runtime, this should look like a stricter typed version of `require_approval`, preserving the current non-widening approval guarantee.

## Example: irreversible-effect approval contract

Irreversible effects are not impossible. They require stronger proof and explicit preview-backed approval.

This contract should be separate from the exact-scope approval contract because reversibility is about proof level and preview semantics, not token scope.

```yaml
id: contract.irreversible_effect_requires_previewed_approval
name: irreversible_effect_requires_previewed_approval
version: 0.1.0
kind: ContractSpec
status: candidate

hook: before_action
severity: hard

match:
  effect.reversibility: irreversible
  env: Env<live>

requires:
  - approval.type == Approval<GrantedFresh>
  - approval.identity == proposal.identity
  - approval.action == proposal.action
  - approval.args_hash == sha256(canonical(proposal.arguments))
  - approval.preview_hash == sha256(rendered_preview)
  - approval.proof_level >= required_proof_level(effect.risk, effect.reversibility)
  - approval.explicit == true

violation:
  type: IrreversibleApprovalRequiredError

repair:
  handlers:
    - skill.request_previewed_approval
  on_repair_failure: block

verify:
  target_type: Approval<GrantedFresh, PreviewBacked, ExactScope>
  verifier_plan: verifier.previewed_approval_exact_scope_valid
```

This avoids a bad loop where `Approval<GrantedFresh>` is obtained but the action still fails because the contract also required `effect.reversibility in [compensable, reversible]`. Reversibility should influence the required proof level, preview, and policy tier; it should not silently make explicitly approved irreversible actions unexecutable.

## Example: entity resolution contract

```yaml
id: contract.entity_use_requires_resolved_entity
name: entity_use_requires_resolved_entity
version: 0.1.0
kind: ContractSpec
status: candidate

hook: before_action
severity: hard

match:
  action in [READ, FINAL, crm.update_customer, github.comment_on_issue]

requires:
  - referenced_entities.all(type == Entity<Resolved>)

violation:
  type: AmbiguousEntityError

repair:
  handlers:
    - skill.resolve_entity_by_context
    - skill.ask_clarifying_question
  on_repair_failure: ask

verify:
  target_type: Entity<Resolved>
  verifier_plan: verifier.entity_unique_against_candidates
```

This catches failures where the model acts on the wrong customer, record, issue, label, company, paper, person, or similarly named web entity.

## Example: code verification contract

```yaml
id: contract.code_final_requires_tests
name: code_final_requires_tests
version: 0.1.0
kind: ContractSpec
status: candidate

hook: before_action
severity: soft

match:
  action: FINAL
  payload_contains: code

applies_when:
  - task.kind in [code_generation, code_patch]

requires:
  - code.syntax == valid
  - tests.status in [passing, not_available_with_reason]
  - edge_cases.reviewed == true

violation:
  type: UntestedCodeError

repair:
  handlers:
    - skill.generate_unit_tests
    - skill.run_available_tests
    - skill.edge_case_walkthrough
  on_repair_failure: warn

verify:
  target_type: Code<Verified>
  verifier_plan: verifier.code_tests_or_reasoned_walkthrough
```

Severity is `soft` because some contexts cannot execute tests. The contract should still produce a warning or force a walkthrough.

## Hard, soft, and audit contracts

Contracts need severity levels to avoid a brittle agent.

```text
hard  = cannot execute until satisfied; used for external side effects and high-risk factual claims
soft  = can execute only with downgrade, warning, or explicit reason
audit = never blocks; emits telemetry and replay fixtures
```

Suggested mapping:

| Severity | Runtime behavior | Example |
|---|---|---|
| `hard` | block or repair before execution | Payment without exact approval |
| `soft` | repair if cheap, otherwise warn and trace | One-source factual answer |
| `audit` | record only | Query was long but still acceptable |

## Interaction with PolicySpec

Contract specs are not a replacement for policy-as-code.

Use `PolicySpec` when:

```text
The rule is organizational authorization or compliance.
Example: amount > 10000 requires approval.
```

Use `ContractSpec` when:

```text
The rule is a reusable agent-state transition invariant with repair semantics.
Example: FINAL requires Answer<Verified>.
Example: Entity<Ambiguous> cannot be used as Entity<Resolved>.
Example: Approval token must match exact call scope before an external send.
```

Some contracts can compile down to policy checks for the v0.1 gateway:

```text
ContractSpec(hard, no repair) -> PolicySpec(enforcement=block)
ContractSpec(hard, repair=request_approval) -> PolicySpec(enforcement=require_approval) + repair handler
ContractSpec(soft) -> PolicySpec(enforcement=warn) + VerifierPlan
```

## Implementation plan

### Phase 0 — documentation only

This document is Phase 0. No runtime behavior changes.

### Phase 1 — data model spike

Add a small typed-state and contract model without changing the gateway hot path.

Candidate files:

```text
schemas/contract_spec.schema.json
src/cak/types.py
src/cak/contracts.py
tests/test_contracts.py
examples/v0_2/contract_specs.yaml
```

Minimal Python objects:

```python
@dataclass(frozen=True, slots=True)
class TypeAtom:
    family: str          # Claim, Answer, Entity, Action, Approval
    state: str           # Verified, Draft, Ambiguous, GrantedFresh
    subject: str | None  # claim id, entity id, action id

@dataclass(frozen=True, slots=True)
class TypedState:
    atoms: tuple[TypeAtom, ...]
    facts: dict[str, object]

@dataclass(frozen=True, slots=True)
class ContractSpec:
    id: str
    hook: str
    severity: str
    match: tuple[str, ...]
    requires: tuple[str, ...]
    violation_type: str
    repair_handlers: tuple[str, ...]
    verifier_plan: str | None

@dataclass(frozen=True, slots=True)
class ContractViolation:
    contract_id: str
    error_type: str
    severity: str
    missing: tuple[str, ...]
    repair_handlers: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ContractDecision:
    ok: bool
    violations: tuple[ContractViolation, ...]
```

### Phase 2 — checker MVP

Implement:

```python
def check_contracts(
    typed_state: TypedState,
    proposal: Proposal,
    contracts: tuple[ContractSpec, ...],
) -> ContractDecision:
    ...
```

Keep predicates deliberately boring. Prefer CEL once the v0.2 policy predicate decision is implemented. Do not invent a full language yet.

### Phase 3 — integrate before existing verifier

The contract checker should run before `verify(config, proposal)` when the proposal depends on agent-state guarantees not visible to `EffectSpec`.

```text
proposal
  -> type_state_from_trace_and_observation
  -> check_contracts
  -> if OK: verify EffectSpec/Capability/PolicySpec
  -> if violation: repair/block/warn
```

For v0.1-compatible SaaS/ops examples, start with external side-effect and approval contracts only.

### Phase 4 — repair router

Add a repair router only after contract violations are observable in traces.

```python
def route_repair(violation: ContractViolation) -> RepairPlan:
    ...
```

Repair execution must go through the same gateway. A repair skill should never bypass capability, policy, or effect checks.

### Phase 5 — verifier-gated type upgrades

Add verifiers that can upgrade typed state:

```text
verifier.approval_token_exact_scope_valid -> Approval<GrantedFresh, ExactScope>
verifier.previewed_approval_exact_scope_valid -> Approval<GrantedFresh, PreviewBacked, ExactScope>
verifier.effect_postcondition_met -> Effect<PostconditionSatisfied>
verifier.answer_supported -> Answer<Verified>
verifier.entity_unique -> Entity<Resolved>
verifier.code_tests_pass -> Code<Verified>
```

Every upgrade should produce a `VerifierReport` and be replayable.

### Phase 6 — learning compiler

Only after Phases 1–5 are stable:

```text
trace failure
  -> failure cluster
  -> typed violation candidate
  -> contract candidate
  -> repair handler candidate
  -> replay tests
  -> promotion queue
```

Admission should follow the same lifecycle as other learned artifacts:

```text
draft -> candidate -> shadow_tested -> verified -> approved -> active
```

## First contracts to prototype

### 1. Unknown effect contract

```text
Any live write action must have an EffectSpec.
```

Why first: it fits the v0.1 gateway and current code.

```text
Action<Write|ExternalSend|Delete|Payment> + Env<Live>
requires EffectSpec<Known>
otherwise UnknownEffectError -> block
```

### 2. Exact fresh approval contract

```text
External side effects require a scoped, fresh approval token that matches the exact call.
```

Why second: this strengthens the approval-token work already present in v0.1.

```text
Action<ExternalSend|Financial|Irreversible>
requires Approval<GrantedFresh, ExactScope>
where scope = identity + action + sha256(canonical arguments)
otherwise MissingApprovalError -> request approval or block
```

### 3. Irreversible preview contract

```text
Irreversible live effects require explicit preview-backed approval at the required proof level.
```

Why third: this preserves the existing governance model: irreversible does not mean impossible, it means stronger approval.

```text
Effect<Irreversible> + Env<Live>
requires Approval<GrantedFresh, ExactScope, PreviewBacked>
otherwise IrreversibleApprovalRequiredError -> request previewed approval or block
```

### 4. Compensation-prepared contract

```text
Compensable actions must have a valid compensation plan before commit.
```

Why fourth: this aligns with the compensation chain already in the demo.

```text
Effect<Compensable>
requires CompensationSpec<Executable>
otherwise MissingCompensationError -> block or require approval
```

These avoid the harder epistemic QA problem while validating the contract architecture inside the v0.1 product wedge.

## Later contracts

After the gateway contracts work, add agent-cognition contracts:

```text
FINAL on factual task requires Answer<Verified>
Entity use requires Entity<Resolved>
Multi-hop answer requires EvidenceChain<Complete>
Code final requires Code<Verified> or explicit no-test reason
Repeated failed search requires query reformulation
Memory write requires EvidenceSpec and ScopeSpec
Skill promotion requires tests, replay, and counterexamples
```

## Telemetry

Each contract activation should emit:

```yaml
contract_event:
  contract_id: contract.final_requires_verified_answer
  proposal_id: proposal_123
  typed_state_hash: ts_abc
  decision: violation
  violation_type: MissingEvidenceError
  severity: hard
  repair_handler: skill.acquire_evidence
  repair_outcome: success | failed | skipped
  target_type_before: Answer<Draft>
  target_type_after: Answer<Verified>
  added_steps: 1
  downstream_outcome: success | failure | unknown
```

Metrics:

```text
activation_count
true_positive_rate
false_positive_rate
repair_success_rate
downstream_success_delta
added_cost
added_latency
overblocking_rate
replay_regression_count
```

## Promotion criteria

A contract should not become active just because it sounds reasonable.

Promotion requires:

```text
1. deterministic trigger or bounded predicate language;
2. positive replay fixtures where it catches a real failure;
3. negative replay fixtures where it must not fire;
4. no capability/policy bypass in repair handler;
5. verifier that can confirm target type or a documented reason why it cannot;
6. false-positive budget;
7. owner and rollback path;
8. evidence and counterexamples;
9. shadow eval before active use.
```

## Non-goals

Do not do these first:

```text
- full dependent type system;
- theorem proving;
- a new general-purpose programming language;
- replacing CEL/Rego/Cedar;
- automatic trace-to-contract generation before contract replay exists;
- letting LLM-generated contracts go active without strict validation;
- treating type confidence as numeric before calibration exists.
```

## Key design risks

### Overblocking

Contracts can make agents safe but useless. Mitigation: hard/soft/audit severities, negative tests, and explicit override policies.

### Grounding gap

A type is only as good as its grounding. `Answer<Verified>` must mean a verifier ran, not that the model claimed confidence.

### Repair loops

A contract can call a repair skill that re-triggers the same contract. Mitigation: attempt caps, repair budgets, and typed progress checks.

### Library pollution

Generated contracts can be too narrow, too broad, redundant, or harmful. Mitigation: same artifact lifecycle, replay, teacher/human review, and quarantine.

### Policy confusion

Some rules belong in `PolicySpec`, not `ContractSpec`. Mitigation: use `PolicySpec` for authorization/compliance and `ContractSpec` for typed agent-state invariants with repair semantics.

### Approval widening

Contracts must preserve exact-call approval scope. Approval for one recipient, amount, invoice, or payload must not authorize another call with the same action name.

## Proposed decision

Adopt contract/type-system skills as a v0.2+ design direction, but keep v0.1 focused on enforceable tool-boundary governance.

Concrete next move:

```text
1. Keep v0.1 verifier unchanged.
2. Add schema/design experiments for ContractSpec as a sibling of SkillSpec.
3. Prototype UnknownEffectError and exact-scope MissingApprovalError.
4. Add irreversible preview/proof-level handling as a separate contract.
5. Only then explore epistemic contracts such as Answer<Verified>.
```

## Short implementation summary

```text
ContractSpec = typed invariant + violation + repair handlers + verifier + replay tests.

The checker does not ask “which memory is semantically similar?”
It asks “is this proposed transition legal in the current typed state?”

If not legal, it emits a type error.
That type error routes to repair.
Repair must be verified before the action is retried.
```
