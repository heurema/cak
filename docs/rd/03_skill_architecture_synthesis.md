# Skill Architecture Deep Research Synthesis

Status: research synthesis, not decision-grade RDR. This document records insights to carry into the RDR-001 research run and future design work. It does not decide a final skill protocol, does not standardize SkillPack, and does not promote ContractSpec beyond experimental status.

## Why this document exists

The first CAK R&D documents created the process: research runs, source ledgers, pattern extraction, adversarial review, debate, and quality gates. This note captures a deeper synthesis from the current skill/procedural-memory references before the next step. It should seed RDR-001, but it is not a substitute for a full research run with source-ledgered claims.

The selected references do **not** point to one single skill format. They split the problem into several layers:

```text
portable package format
runtime-control object
verifier/proof obligation
stage-aware procedural memory
compositional skill graph
provenance/governance graph
execution-grounded repair loop
security/admission boundary
```

The central emerging hypothesis is:

```text
CAK skills should be compiled artifacts, not directly trusted authored artifacts.

Authored material:
  package, script, workflow, trace, contract draft, repair note

Compiled admitted artifact:
  Runtime IR fragment
  + Evidence IR links
  + verifier obligations
  + security envelope
  + lifecycle state
```

## Core synthesis

### Skill is not one artifact

A skill for an AI agent should not be collapsed into any single representation:

```text
skill != package
skill != function
skill != workflow
skill != contract
skill != prompt text
```

A stronger working definition:

```text
Agent-native skill = a verified, state-conditioned bridge between evidence and future behavior.
```

This implies the skill system needs at least two internal surfaces:

```text
Evidence / Provenance IR:
  traces
  documents
  source ledgers
  failure ledgers
  diagnoses
  counterexamples
  historical versions
  governance records

Runtime / Control IR:
  contracts
  hooks
  state predicates
  actions
  effects
  permissions
  verifier plans
  lifecycle state
  activation and repair policies
```

A skill bridges these spaces. Evidence explains why the skill exists and when it worked or failed. Runtime IR decides when and how it affects agent behavior.

### Why this differs from human software

Human software usually assumes that source files, packages, documentation, tests, and APIs are authored primarily for humans. AI-agent skills are different because a skill can simultaneously be:

```text
instruction
memory
policy influence
runtime behavior patch
code execution surface
permission request
self-modification input
supply-chain artifact
```

Therefore, CAK should separate:

```text
authoring
import
compilation
admission
activation
evolution
retirement
```

A user or model may author a skill. CAK should only activate an admitted, compiled artifact after validation, replay, verifier checks, security review, and lifecycle gating.

## Reference-derived insights

## 1. VASO: contracts need verifier-facing and planner-facing views

Reference: [VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](https://arxiv.org/abs/2606.05395)

### Pattern to inspect

VASO represents reusable robot skills as semantic contracts with two coupled interfaces:

```text
formal / verifier-facing interface:
  aligns robot states, observations, and controls with logical propositions
  supports model checking against temporal specifications

planner-facing interface:
  guides executable behavior generation
```

It performs skill-level feasibility checking, plan-level verification, and uses model-checker counterexample traces as feedback to update reusable skill contracts while keeping foundation-model weights frozen.

### CAK insight

ContractSpec should probably evolve from:

```text
match + requires + violation + repair metadata
```

into a proof-carrying contract artifact:

```text
ProofCarryingContract =
  ContractSpec
  + GroundingSpec
  + VerifierObligations
  + CounterexampleLedger
  + PlannerFacingRepairHints
  + ConcurrencyAssumptions
```

### What to copy

- Dual-interface design: runtime/planner side and verifier side.
- Counterexample traces as reusable artifact-improvement signals.
- Frozen-weight external evolution: update the artifact, not only the model.
- Local and global specifications as separate verification concerns.

### What not to copy blindly

- Robotics-specific proposition labeling assumptions.
- Strong formal-verification claims without grounding guarantees.
- Sequential-only assumptions if CAK later supports interleaved or concurrent skills.

### CAK adaptation

A CAK contract should declare not just what it checks, but also:

```yaml
contract:
  runtime_predicates: [...]
  verifier_obligations: [...]
  grounding_assumptions: [...]
  counterexample_traces: [...]
  repair_affordances: [...]
  concurrency_assumptions: sequential | interleaved | unknown
```

### RDR questions informed

- RDR-003: What is ContractSpec really?
- RDR-016: Verifier-gated type upgrades.
- RDR-011: Proof-carrying skills.

### Caution

A verified contract is only as good as its grounding. If the mapping from runtime state to propositions is wrong, verification can approve unsafe behavior.

## 2. Programmatic Skill Networks: skill libraries are graphs with lifecycle semantics

Reference: [Evolving Programmatic Skill Networks](https://arxiv.org/abs/2601.03509)

### Pattern to inspect

PSN treats skills as executable symbolic programs arranged into a compositional network. It adds:

```text
Reflect:
  structured fault localization over composed skills

maturity-aware update gating:
  stable skills are protected from noisy downstream updates
  uncertain skills remain plastic

structural refactoring with rollback validation:
  merge, split, or refactor network structure
  revert if validation degrades
```

### CAK insight

A skill library should not be a flat registry. It should be a SkillGraph:

```text
SkillGraph =
  skill nodes
  dependency edges
  maturity states
  health metrics
  fault attribution
  rollback checkpoints
  conflict edges
  refactoring operations
```

### What to copy

- Dependency-aware composition.
- Maturity levels and update gating.
- Fault localization across composed skills.
- Rollback validation before accepting structural refactors.
- Library compactness as a health metric.

### What not to copy blindly

- Assuming symbolic programs can always model ambiguous LLM-agent state.
- Treating empirical rollback validation as a formal guarantee.
- Allowing automatic refactors without verifier/replay/security gates.

### CAK adaptation

Future CAK skill nodes should probably carry:

```yaml
skill_node:
  id: skill.resolve_entity
  kind: executable | intervention | contract | workflow | verifier | stage
  maturity: draft | candidate | stable | protected | deprecated | quarantined
  dependencies:
    requires: []
    calls: []
    conflicts_with: []
  evidence:
    source_traces: []
    repair_traces: []
    counterexamples: []
  lifecycle:
    update_policy: plastic | gated | frozen
    rollback_checkpoint: ...
    health_score: ...
```

### RDR questions informed

- RDR-014: Skill lifecycle and ecology.
- RDR-018: Skill conflict detection and composition.
- RDR-005: Skill library pollution.

### Caution

PSN strengthens the lifecycle story but not the full trust story. CAK should combine graph/lifecycle mechanisms with verifier obligations and security admission.

## 3. HMT: workflow memory should be stage-aware and state-conditioned

Reference: [Enhancing Web Agents with a Hierarchical Memory Tree](https://arxiv.org/abs/2603.07024)

### Pattern to inspect

HMT diagnoses flat memory as entangling high-level task logic with site-specific action details. It constructs a three-level hierarchy:

```text
Intent:
  normalized task goal

Stage:
  reusable semantic subgoal
  observable preconditions
  observable postconditions

Action:
  action pattern
  transferable semantic element description
```

At inference time, a Planner uses pre/postconditions to align the current page with the correct stage, while an Actor grounds actions on the current interface.

### CAK insight

Workflow-like skills should not be represented as linear macros. They should compile into stage-aware structures:

```text
Intent -> Stage -> Action
```

or into guarded automata / StageSpecs:

```yaml
StageSpec:
  intent: resolve_place_entity
  preconditions:
    - place_entity.type in [Unknown, Ambiguous]
  postconditions:
    - place_entity.type == Resolved
  allowed_actions:
    - SEARCH
    - READ
  grounding:
    semantic_selectors: true
  verifier:
    plan: verifier.entity_unique_against_candidates
```

### What to copy

- Separate task intent from semantic stage and environment-specific action grounding.
- Use observable preconditions and postconditions for retrieval and execution.
- Use stage-aware Planner/Actor split.
- Avoid raw element IDs or brittle action traces as transferable memory.

### What not to copy blindly

- Web-only assumptions.
- Overconfidence that semantic descriptions always ground correctly.
- Linear workflows as the internal representation.

### CAK adaptation

CAK should consider adding a `StageSpec` or `ProcedureStage` concept before standardizing workflow skills.

```text
WorkflowSkill -> StageGraph -> Runtime hooks + verifiers
```

### RDR questions informed

- RDR-006: Retrieval by state, not just semantics.
- RDR-007: Workflow, state machine, behavior tree, or Program Function?
- RDR-001: What is an agent-native skill?

### Caution

The transferable unit is not the full action sequence; it is the stage abstraction plus grounding strategy.

## 4. Agent Skills format: useful outer package, insufficient runtime semantics

References:

- [Agent Skills specification](https://agentskills.io/)
- [SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior](https://arxiv.org/abs/2606.11543)
- [SkillReducer: Optimizing LLM Agent Skills for Token Efficiency](https://arxiv.org/abs/2603.29919)

### Pattern to inspect

Agent Skills-style packages emphasize:

```text
SKILL.md
scripts/
references/
assets/
frontmatter metadata
progressive disclosure
routing description
host compatibility
```

SkillJuror and SkillReducer are useful follow-on references because they show that organization, routing descriptions, and progressive disclosure affect runtime behavior and token efficiency.

### CAK insight

Agent Skills is a good **outer distribution layer**, not the full semantics of skill.

```text
External package:
  SKILL.md
  scripts/
  references/
  assets/

CAK import compiler:
  parse package
  classify artifact types
  extract permissions
  build ContractSpec / SkillSpec / VerifierPlan / StageSpec
  attach provenance
  run admission tests
  mark active / shadow / rejected / quarantined
```

### What to copy

- Simple package ergonomics.
- Progressive disclosure and context economy.
- Separation of scripts, references, and assets.
- Host compatibility metadata as a distribution concern.

### What not to copy blindly

- Treating human-readable markdown as sufficient for runtime control.
- Treating package validation as admission.
- Treating routing description as reliable state-conditioned activation.
- Allowing scripts/assets without security envelope.

### CAK adaptation

Skill packaging should compile into CAK-native IR. A package should not be directly active.

```text
Package imported != skill admitted != skill activated
```

### RDR questions informed

- RDR-009: Should SkillPack become a separate protocol/project?
- RDR-015: Skill security and supply chain.
- RDR-001: What is an agent-native skill?

### Caution

The outer package can make skills portable, but only internal runtime/evidence/security layers make them reliable.

## 5. SkillWiki: skill ecosystems need provenance and governance

Reference: [SkillWiki: A Living Knowledge Infrastructure for Agent Skills](https://arxiv.org/abs/2606.16523)

### Pattern to inspect

SkillWiki separates:

```text
knowledge layer:
  documents
  trajectories
  API specs
  scripts
  historical skills
  execution records

skill layer:
  derived structured skills
  versions
  validations
  dependencies
  releases
```

It introduces a Skill Provenance Graph linking knowledge sources, skills, executions, validations, versions, and dependencies. It also uses a Git-style governance workflow for repairs, decompositions, replacements, releases, deprecations, and archives.

### CAK insight

A skill registry is not enough. CAK needs a Skill Provenance Graph:

```text
source document -> knowledge claim -> skill candidate
trace -> diagnosis -> repair
skill version -> execution -> validation
failed execution -> counterexample -> new version
new version -> admitted / rejected / quarantined
old version -> deprecated / archived
```

### What to copy

- Separate knowledge artifacts from runtime-active skills.
- Provenance graph across sources, skills, executions, validations, and versions.
- Governance workflow for repair, release, deprecation, and archive.
- Auditable skill lifecycle events.

### What not to copy blindly

- Building registry infrastructure before runtime evidence.
- Treating governance UI as the main product before admission semantics are proven.

### CAK adaptation

CAK should model skill provenance as first-class metadata even before it has a marketplace or registry.

```yaml
provenance:
  originating_sources: []
  originating_traces: []
  diagnoses: []
  validations: []
  versions: []
  dependencies: []
  deprecation_reason: ...
```

### RDR questions informed

- RDR-014: Skill lifecycle and ecology.
- RDR-015: Skill security and supply chain.
- RDR-019: Telemetry and utility estimation.

### Caution

Infrastructure should follow evidence-backed runtime semantics, not precede them.

## 6. SkillRevise: skill evolution needs diagnosis and preserve ledgers

Reference: [SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision](https://arxiv.org/abs/2606.01139)

### Pattern to inspect

SkillRevise is about improving an imperfect initial skill. It uses:

```text
Diagnosis object:
  execution evidence
  verification requirements
  failure attribution
  preservation constraints

Principle memory:
  reusable repair principles

Execution-anchored edits:
  revisions tied to observed behavior

Re-execution and utility retention:
  keep best observed candidate
```

### CAK insight

Skill evolution should not mean “rewrite the skill.” It should mean:

```text
failed execution
-> diagnosis
-> preserve ledger
-> candidate edits
-> re-execution
-> utility comparison
-> accept / reject / quarantine
```

### What to copy

- Diagnosis artifact as a structured repair input.
- Preserve ledger to protect previously passing behavior.
- Execution anchors that tie edits to observable runtime changes.
- Utility-gated best-of-N retention.
- Cross-model transfer measurement as a cautionary signal.

### What not to copy blindly

- Assuming revised skills transfer uniformly across agents or models.
- Accepting revisions based only on recent failure cases.
- Ignoring regressions on previous passing traces.

### CAK adaptation

Introduce a future `SkillDiagnosis` / `PreserveLedger` concept:

```yaml
skill_diagnosis:
  failed_skill: skill.x
  trace_id: trace.123
  expected_postconditions: []
  observed_failure: ...
  blamed_component: activation | precondition | action_body | verifier | grounding | dependency
  preserve:
    passing_cases: []
    behavior_that_must_not_change: []
  candidate_edits: []
  reexecution_results: []
  decision: accept | reject | quarantine | request_more_evidence
```

### RDR questions informed

- RDR-005: Skill library pollution.
- RDR-014: Skill lifecycle and ecology.
- RDR-019: Telemetry and utility estimation.

### Caution

Repair without preserve constraints can overfit and pollute the library.

## 7. Security analyses: external skills are a supply-chain and prompt-injection surface

References:

- [Agent Skills Enable a New Class of Realistic and Trivially Simple Prompt Injections](https://arxiv.org/abs/2510.26328)
- [Malicious Or Not: Adding Repository Context to Agent Skill Classification](https://arxiv.org/abs/2603.16572)

Additional references to inspect:

- SkillJect / skill-based prompt injection work.
- Large-scale agent skill ecosystem vulnerability analyses.

### Pattern to inspect

Security analyses point to risks such as:

```text
malicious SKILL.md instructions
hidden payloads in helper scripts
long-file prompt injection
repository-context mismatch
abandoned repository hijacking
approval widening
"do not ask again" hazards
skill marketplace trust failures
```

### CAK insight

Skill import is a security boundary. CAK should separate:

```text
authoring
import
static scan
sandbox execution
verifier checking
replay/shadow testing
admission
activation
evolution
quarantine / rollback
```

### What to copy

- Context-aware authorization rather than only static filtering.
- Repository/source context in skill classification.
- Exact-scope approval semantics.
- Treat scripts and references as executable influence surfaces.
- Quarantine and rollback as normal lifecycle paths.

### What not to copy blindly

- Trusting marketplace metadata.
- Relying only on model-based malicious/benign classification.
- Assuming bigger models or simple filters solve prompt injection.

### CAK adaptation

Every external skill package should have a security envelope:

```yaml
trust:
  source: local | repo | marketplace | generated | imported
  signed: true | false
  provenance_complete: true | false
  contains_scripts: true | false
  requested_tools: []
  requested_permissions: []
  data_access: []
  side_effects: []
  approval_scope: exact | broad | unknown
  sandbox_required: true
  admission_status: authored | parsed | scanned | shadow | active | quarantined
```

### RDR questions informed

- RDR-015: Skill security and supply chain.
- RDR-009: Should SkillPack become a separate protocol/project?
- RDR-011: Proof-carrying skills.

### Caution

Portable skill formats increase distribution, but distribution without admission and authorization increases risk.

## 8. HASP, AWM, and Voyager as core anchors

These were already in the CAK R&D anchors, but the newer references sharpen their interpretation.

### HASP

Reference: [Harnessing LLM Agents with Skill Programs](https://arxiv.org/abs/2605.17734)

HASP shows that passive textual skills can be ignored or applied unreliably. Its Program Functions expose `should_activate` and `intervene`, modify actions or inject context, emit structured intervention signals, and require strict validation/filtering to prevent skill library pollution.

CAK adaptation:

```text
Active skills should be runtime-control objects with:
  hooks
  activation predicates
  intervention modes
  audit records
  rate limits
  validation gates
  rollback/quarantine
```

### AWM

Reference: [Agent Workflow Memory](https://arxiv.org/abs/2409.07429)

AWM shows that workflow memory can improve web agents and that abstract reusable workflows can outperform concrete examples, but it also shows that workflows can bias actions and that agents must learn when to diverge from workflow guidance.

CAK adaptation:

```text
Workflow memory should become guarded StageGraph, not fixed macro.
```

### Voyager

Reference: [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)

Voyager shows that executable code skills, self-verification, iterative environment feedback, and an external skill library can support lifelong learning without weight updates in a stable API environment.

CAK adaptation:

```text
Executable skills are strongest when:
  API is stable
  verifier exists
  execution feedback is available
  composition dependencies are explicit
```

## Architecture hypotheses for CAK

## H1: Skill as compiled bridge

```text
Skill = compiled bridge between Evidence IR and Runtime IR.
```

Why strong:

- Explains why package, runtime, verifier, provenance, and lifecycle layers are all needed.
- Prevents authored packages from becoming active by default.
- Supports multiple internal forms: ContractSpec, SkillSpec, StageSpec, VerifierPlan, PolicySpec.

## H2: Package outside, typed runtime inside

```text
External package format can be Agent Skills-compatible.
Internal CAK runtime should use richer IR.
```

Why strong:

- Gives portability without sacrificing verifier/security semantics.
- Avoids premature SkillPack standardization.

## H3: Flat registry is wrong; SkillGraph is likely needed

```text
Skill library should include dependencies, maturity, health, rollback, provenance, and conflicts.
```

Why strong:

- PSN, SkillWiki, SkillRevise, and security analyses all point away from flat lists.

## H4: Workflow skills should compile to StageGraph

```text
Linear workflow -> guarded stage-aware memory -> grounded action.
```

Why strong:

- HMT and AWM both show that workflow retrieval must respect current state.

## H5: ContractSpec should become proof-carrying

```text
ContractSpec = runtime predicate + verifier obligation + counterexample ledger.
```

Why strong:

- VASO directly supports a dual-interface contract model.

## H6: Skill evolution needs diagnosis/preserve/admission

```text
skill failure -> diagnosis -> candidate repair -> preserve tests -> replay -> admit or quarantine
```

Why strong:

- SkillRevise and HASP both warn against uncontrolled evolution.

## H7: Skill import is a security boundary

```text
external skill package != trusted runtime artifact
```

Why strong:

- Agent Skills security research shows portable skills can be prompt-injection and supply-chain surfaces.

## Proposed future CAK components to investigate

These are **not decisions**. They are candidate concepts for RDRs and experiments.

```text
Runtime IR:
  ContractSpec
  SkillSpec
  StageSpec
  VerifierPlan
  PolicySpec
  HookSpec
  EffectSpec

Evidence IR:
  SourceLedger
  TraceLedger
  FailureLedger
  CounterexampleLedger
  SkillDiagnosis
  PreserveLedger
  ProvenanceGraph

Lifecycle / governance:
  SkillGraph
  SkillMaturity
  SkillHealth
  RefactorProposal
  RollbackCheckpoint
  QuarantineRecord

Security:
  SkillTrustEnvelope
  PermissionManifest
  SandboxProfile
  ExactScopeApproval
  SupplyChainScan

Compilation / admission:
  SkillImportCompiler
  SkillAdmissionPipeline
  ReplayGate
  ShadowMode
  UtilityGate
```

## Candidate artifact pipeline

```text
Authored / discovered material
  Agent Skills-like package
  workflow trace
  code skill
  paper/API docs
  failure trace
  repair note

-> Evidence IR
  source ledger
  trace ledger
  claim/pattern matrix
  failure diagnosis
  counterexamples
  provenance graph

-> Compilation
  classify artifact type
  extract permissions
  extract pre/postconditions
  extract verifier obligations
  extract runtime hooks
  link evidence

-> Runtime IR
  ContractSpec
  SkillSpec
  StageSpec
  VerifierPlan
  PolicySpec
  HookSpec

-> Admission
  static/security scan
  syntax/interface check
  mock execution
  verifier check
  replay/shadow test
  utility/overblocking check

-> Activation
  state-conditioned retrieval
  contract/type-error routing
  hook execution
  repair or intervention
  trace/audit event

-> Evolution
  diagnosis
  candidate repair
  preserve ledger
  re-execution
  rollback validation
  maturity update
  quarantine or promotion
```

## How this changes RDR-001

Original question:

```text
What is an agent-native skill?
```

Updated working hypothesis:

```text
An agent-native skill is a compiled, governed bridge between evidence/provenance and runtime control.
```

Competing hypotheses to compare:

```text
H1: skill = portable package
H2: skill = executable code/program
H3: skill = runtime intervention / Program Function
H4: skill = proof-carrying contract
H5: skill = stage-aware procedural memory
H6: skill = governed lifecycle node in SkillGraph
H7: skill = compiled bridge artifact
```

## Minimal experiment sketch for RDR-001

Take the same failure traces and encode repairs in multiple forms:

```text
A. Agent Skills-style package
B. ContractSpec
C. Program Function / runtime intervention
D. StageGraph / HMT-like procedural memory
E. SkillGraph node with maturity/provenance
F. compiled hybrid artifact
```

Compare:

```text
activation precision
verifier coverage
repair success
transfer across task variants
overblocking
runtime cost
provenance completeness
security/admission risk
mutation/repair safety
replay stability
human review burden
```

## Non-decisions

Do not conclude yet that:

```text
- SkillPack should be standardized.
- Agent Skills format is sufficient.
- ContractSpec is the central abstraction.
- Program Functions are always better than workflows.
- Workflow memory should be linear.
- A flat skill registry is adequate.
- External skills can be trusted after format validation.
```

## Recommended next step

Before implementing more runtime features, bootstrap the RDR-001 research run with this synthesis as an input:

```text
docs/rd/runs/rdr_001_agent_native_skill/
  research_plan.md
  source_ledger.yaml
  pattern_matrix.md
  claim_matrix.md
  hypothesis_matrix.md
  adversarial_review.md
  debate.md
  decision_packet.md
```

The research run should explicitly test the working hypothesis:

```text
Skill = compiled bridge between Evidence IR and Runtime IR.
```

It should also adversarially test whether this is overengineering compared with simpler alternatives such as Agent Skills-style packages, Program Functions, or ContractSpec-only designs.

## Reference anchors

Primary references already inspected or marked for source-ledger inspection:

- VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents — https://arxiv.org/abs/2606.05395
- Evolving Programmatic Skill Networks — https://arxiv.org/abs/2601.03509
- Enhancing Web Agents with a Hierarchical Memory Tree — https://arxiv.org/abs/2603.07024
- Agent Skills specification — https://agentskills.io/
- SkillWiki: A Living Knowledge Infrastructure for Agent Skills — https://arxiv.org/abs/2606.16523
- SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision — https://arxiv.org/abs/2606.01139
- Agent Skills Enable a New Class of Realistic and Trivially Simple Prompt Injections — https://arxiv.org/abs/2510.26328
- Malicious Or Not: Adding Repository Context to Agent Skill Classification — https://arxiv.org/abs/2603.16572
- SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior — https://arxiv.org/abs/2606.11543
- SkillReducer: Optimizing LLM Agent Skills for Token Efficiency — https://arxiv.org/abs/2603.29919
- Harnessing LLM Agents with Skill Programs — https://arxiv.org/abs/2605.17734
- Agent Workflow Memory — https://arxiv.org/abs/2409.07429
- Voyager: An Open-Ended Embodied Agent with Large Language Models — https://arxiv.org/abs/2305.16291

These links are reference anchors, not yet a complete source ledger. RDR-001 should convert relevant anchors into explicit claim/pattern entries with inspected passages, limitations, confidence, and counterevidence.
