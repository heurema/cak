# CAK R&D Question Map

This file records open questions before CAK turns skills and procedural memory
into a protocol or product surface. The central question for each major design
is:

Does the human-software default transfer to AI agents, or do we need an
agent-native abstraction?

## P0 - Foundational questions

### RDR-001 - What is an agent-native skill?

Research question:
What is a skill for an AI agent: text advice, workflow, executable code,
intervention function, contract, verifier, type transition, causal
intervention, or a package that combines these?

Why it matters:
If the core unit is wrong, every registry, protocol, verifier, and runtime hook
will be wrong.

Human default:
A skill is usually documentation, training, package, function, or macro.

Why human default may fail:
Agents may ignore documentation, misuse macros, call functions at the wrong
time, or lack verifier evidence.

Hypotheses:

- H1: skill = reusable executable behavior.
- H2: skill = state-conditioned runtime intervention.
- H3: skill = proof-carrying typed transition.
- H4: skill = package containing behavior + contract + verifier + tests + telemetry.

Weird alternatives:

- Skill as runtime patch.
- Skill as type-error handler.
- Skill as trace theorem.
- Skill as causal intervention.
- Skill as ecological organism with birth/fitness/retirement.

Minimal experiment:
Compare text-only, workflow, executable program, Program Function,
ContractSpec, and hybrid on the same failure traces.

### RDR-002 - Active vs passive skills

Research question:
When should skills be passively retrieved into context, and when should they
actively intervene in the agent loop?

Mechanisms to compare:

- passive memory
- prompt guidance
- context injection
- action override
- tool-call blocking
- repair routing
- verifier-triggered retry

Key concern:
Passive text may be cheap and flexible but unreliable. Active skills may be
reliable but risk overblocking and false positives.

### RDR-003 - What is ContractSpec really?

Research question:
Is ContractSpec a skill, policy, type rule, verifier precondition, exception
handler, or CAK-native artifact?

Hypotheses:

- ContractSpec as sibling of SkillSpec.
- ContractSpec compiled into PolicySpec.
- ContractSpec as type checker rule.
- ContractSpec as exception routing table.
- ContractSpec as proof obligation.

Minimal experiment:
Try expressing the same invariant as PolicySpec, SkillSpec, ContractSpec, and
VerifierPlan; compare clarity, validation, runtime behavior, and replay.

### RDR-004 - Experience as source code

Research question:
Can agent traces be treated as source code for future behavior?

Pipeline:

```text
experience trace
-> segmentation
-> failure/success abstraction
-> causal hypothesis
-> skill candidate
-> verifier
-> replay tests
-> runtime admission
```

Weird alternatives:

- Trace calculus.
- Experience compiler.
- Skill as compiled object file.
- Verifier as type checker.
- Telemetry as optimizer.

### RDR-005 - Skill library pollution

Research question:
How do we prevent a lifelong agent from corrupting itself with too many, too
broad, too narrow, or harmful skills?

Mechanisms to study:

- admission gates
- syntax/interface/mock execution
- teacher/human review
- counterexample tests
- shadow mode
- utility thresholds
- quarantine
- retirement
- conflict detection
- library size caps
- versioning and rollback

### RDR-006 - Retrieval by state, not just semantics

Research question:
Should skill retrieval be semantic, state-based, type-error-based, causal, or
hybrid?

Compare:

- embedding similarity over skill descriptions
- typed-state predicate matching
- failure-signature matching
- type-error routing
- causal graph retrieval
- learned selector
- teacher-assisted selector

### RDR-007 - Workflow, state machine, behavior tree, or Program Function?

Research question:
What should replace linear workflows in dynamic environments?

Human default:
workflow = fixed step list.

Agent problem:
Dynamic UI, popups, partial observations, missing elements, and changing state
make linear workflows brittle.

Alternatives:

- guarded workflow
- state machine
- behavior tree
- hierarchical task network
- Program Function
- contract-driven repair
- real-time stateful macro

### RDR-008 - External memory vs internalized behavior

Research question:
When should a skill remain external and auditable, and when should it be
internalized into model weights or policy?

Topics:

- external first
- telemetry before distillation
- internalize stable behavior-correcting skills
- keep input-dependent or safety-critical skills external
- rollback and audit concerns

### RDR-009 - Should SkillPack become a separate protocol/project?

Research question:
Should portable skill format become an independent project, or remain inside
CAK?

Current tentative answer:
Not yet. Build inside CAK with extraction boundaries. Extract only after proof
with at least two runtimes or conformance tests.

Evaluation:

- one runtime = internal API
- two runtimes = candidate protocol
- conformance tests = standardization candidate

### RDR-010 - Agent-native programming language

Research question:
What would a programming language for AI agents look like if it were not based
on human-first assumptions?

Possible primitives:

- hooks
- typed state
- contracts
- actions
- effects
- verifiers
- traces
- telemetry
- repair handlers
- causal hypotheses
- budget/risk types

Weird alternatives:

- eBPF for agent loops
- exception handling for cognition
- proof-carrying skills
- causal patch language
- trace-oriented programming

## P1 - Mechanism questions

### RDR-011 - Proof-carrying skills

- Ask whether an active skill should carry machine-checkable preconditions,
  postconditions, tests, replay evidence, or verifier obligations.
- Matters because self-asserted skill confidence is weak evidence.
- Should distinguish proof at authoring time from proof at runtime admission.
- Needs a clear failure mode when evidence expires or no longer transfers.

### RDR-012 - Runtime hook model / agent eBPF

- Ask what hooks an agent loop should expose for observation, retrieval,
  intervention, blocking, repair, replay, and audit.
- Matters because passive documents cannot reliably control behavior.
- Should study a minimal hook set before inventing a full protocol.
- Must preserve sandbox, permission, and data-boundary constraints.

### RDR-013 - Causal SkillGraph

- Ask whether skills should be linked by causal claims: what failure they
  prevent, what state they require, what action they change, and what evidence
  supports that claim.
- Matters because semantic similarity can activate the wrong skill for the
  wrong reason.
- Should support counterexamples, conflict detection, and retirement.
- Could become the bridge between traces, skills, and verifiers.

### RDR-014 - Skill lifecycle and ecology

- Ask how skills are born, admitted, measured, versioned, quarantined, merged,
  deprecated, and retired.
- Matters because a lifelong library can decay even if each individual skill
  looked useful when created.
- Should define shadow-mode measurement and utility thresholds.
- Should avoid treating "more skills" as automatic progress.

### RDR-015 - Skill security and supply chain

- Ask how untrusted or third-party skills are parsed, sandboxed, verified,
  permissioned, signed, updated, and revoked.
- Matters because active skills can become code execution, data exfiltration,
  or policy bypass paths.
- Should separate package trust from runtime admission.
- Needs rollback and audit trails for each admitted version.

### RDR-016 - Verifier-gated type upgrades

- Ask whether an agent state can move to a more privileged or capable type only
  after verifier evidence is present.
- Matters because runtime authority should follow checked state, not model
  confidence.
- Should compare PolicySpec predicates, ContractSpec obligations, and explicit
  verifier plans.
- Needs replay stability and clear downgrade behavior.

### RDR-017 - Repair loop control and oscillation prevention

- Ask how active skills and verifiers avoid infinite retry, tool-call ping-pong,
  or repeated unproductive fixes.
- Matters because repair mechanisms can amplify failures if they lack budgets,
  stop conditions, and evidence thresholds.
- Should track repair attempts as first-class trace events.
- Needs kill criteria for repair handlers and skill-triggered retries.

### RDR-018 - Skill conflict detection and composition

- Ask how two skills compose when they both trigger, disagree, or compete for
  action override.
- Matters because a skill library is a control system, not a bag of notes.
- Should study precedence, typed effects, conflict tests, and human review.
- Needs a way to explain why one skill won or why both were suppressed.

### RDR-019 - Telemetry and utility estimation

- Ask what runtime telemetry is enough to estimate whether a skill is useful,
  harmful, stale, or overactive.
- Matters because admitted skills need ongoing evidence, not one-time approval.
- Should separate correlation from causal utility.
- Needs cost, latency, intervention, success, rollback, and human-review metrics.

### RDR-020 - Multi-agent skill delegation and authority inheritance

- Ask whether one agent can delegate skills, permissions, memory, or verifier
  obligations to another agent.
- Matters because multi-agent systems can launder authority through delegation.
- Should model inherited constraints, revocation, provenance, and audit.
- Needs explicit rules for cross-agent skill reuse and conflict handling.

## P2 - Evaluation questions

- What benchmarks should CAK use for skill systems?
- How do we measure activation precision/recall?
- How do we measure prevented failures?
- How do we estimate causal utility?
- How do we measure overblocking?
- How do we detect memory/skill pollution?
- How do we evaluate transfer across domains?
- How do we compare semantic retrieval vs typed retrieval?
- How do we test untrusted skill packages?

## First recommended RDRs to write

1. RDR-001 - What is an agent-native skill?
2. RDR-003 - What is ContractSpec really?
3. RDR-005 - Skill library pollution.
4. RDR-006 - Retrieval by state, not just semantics.
5. RDR-009 - Should SkillPack become a protocol/project?
