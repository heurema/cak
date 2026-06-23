# Adversarial Review — RDR-001 Agent-Native Skill

Status: exploratory red-team review. This does not decide RDR-001.

## Assumption 1: Skill as compiled bridge is not overengineering

The compiled-bridge hypothesis may be too complex for CAK's current stage. It
combines package structure, runtime hooks, verifier obligations, security
review, provenance, lifecycle, and telemetry before CAK has proven that a
simple package plus tests fails. A broad bridge artifact could become a schema
graveyard: every source contributes a field, but no field is load-bearing.

The most likely failure is that CAK designs a rich artifact without a minimal
runtime experiment. If the first real use case only needs a small `SKILL.md`
with one deterministic helper script and a few tests, the bridge model may slow
learning rather than improve it.

## Assumption 2: CAK needs both Evidence IR and Runtime IR

One IR might be enough. A package manifest could carry provenance, tests,
permissions, and hooks. A ContractSpec could carry runtime and evidence fields.
A Program Function record could include the trace that produced it. Splitting
Evidence IR and Runtime IR may create extra translation and synchronization
work.

The counterargument is that evidence and runtime control evolve at different
rates. Still, this must be tested. If a single append-only skill manifest can
support import, admission, replay, and activation cleanly, the dual-IR split is
unnecessary.

## Assumption 3: Agent Skills is insufficient

Agent Skills-style packaging may be enough for v0.1/v0.2 interoperability.
Progressive disclosure, `SKILL.md`, bundled scripts, resources, and security
guidance already cover a large amount of practical behavior. SkillJuror and
SkillReducer suggest that organization and routing quality can change runtime
behavior without inventing a new compiled artifact model.

The strongest simple path is: adopt a package shell, add strict tests,
provenance, and a deny-by-default execution policy, then defer Runtime IR until
there are enough failures. This may be cheaper than designing bridge semantics
upfront.

## Assumption 4: ContractSpec should become proof-carrying

This may overfit VASO and robotics. VASO has robot states, observations,
control commands, and temporal specifications. CAK may operate over text,
files, APIs, repository state, and human approvals where propositions are
ambiguous or expensive to ground.

Proof-carrying ContractSpec could create false confidence if the proof is over
the wrong abstraction. A contract that verifies a simplified state model may
still permit harmful action in the real tool environment. ContractSpec should
remain a candidate verifier facet until CAK has concrete traces where proof
obligations add value.

## Assumption 5: StageGraph is needed

Workflows plus retrieval may be enough. HMT's stage-aware memory targets web
agents and unseen website generalization. CAK might not need a full StageGraph
if its early workflows are short, API-shaped, or already guarded by tests.

StageGraph also depends on observable preconditions/postconditions. If CAK
cannot observe the state needed to validate a stage, StageGraph becomes a more
formal-looking workflow with the same activation errors.

## Assumption 6: SkillGraph is needed

Maturity, rollback, provenance, dependencies, and conflicts can be deferred.
For a small skill set, a flat allowlist plus quarantine may outperform a
SkillGraph. A graph can become governance overhead before there is enough
volume for graph structure to matter.

The strongest reason to add SkillGraph later is library pollution. But the
first RDR should not assume that CAK will have uncontrolled self-evolving skill
volume. The minimal experiment should compare flat quarantine to lifecycle
graph mechanics before adopting graph language.

## Assumption 7: security/admission should be designed early

Early security design can slow exploration, especially if every candidate skill
needs sandboxing, scanner output, provenance review, and replay before it can
be tested. For local prototypes, it may be faster to run skills manually in a
trusted checkout and record failures.

The opposing risk is that skills mix instructions, code, resources, and tool
authority. SkillInject, SkillJect, MalSkillBench, repository-context analyses,
and the Agent Skills docs make it hard to justify importing untrusted active or
executable skills without at least a minimal admission boundary. The open
question is how small that boundary can be.

## Strongest objections

- The compiled bridge may be a post-hoc synthesis that explains everything and
  predicts too little.
- A package shell plus tests, provenance, and deny-by-default execution may be
  enough for the next CAK milestone.
- Program Functions, ContractSpec, StageGraph, and SkillGraph may be separate
  tools, not facets of one object.
- Security evidence argues for caution, but not necessarily for a complex
  compiled artifact.

## Missing evidence

- Full-paper inspection for HASP, AWM, Voyager, VASO, PSN, HMT, SkillWiki,
  SkillRevise, SkillJuror, SkillReducer, and the security papers.
- Implementation repo inspection for Voyager, SkillWiki, SkillJuror, and any
  available skill-security datasets.
- Negative results where package+tests beats richer runtime intervention.
- Concrete CAK failure traces that require active intervention or typed
  pre/postconditions.
- Older planning/cognitive architecture evidence: STRIPS, ADL, HTN, Soar, and
  production systems.

## Missing counterexamples

- A text-only skill that outperforms active intervention because runtime state
  is ambiguous.
- A package + tests workflow that is sufficient and cheaper than compiled IR.
- A ContractSpec that proves the wrong thing because grounding is incomplete.
- A StageGraph that cannot observe its own preconditions.
- A SkillGraph that adds review work without reducing library pollution.
- A security gate that blocks useful experimentation more than it reduces risk.

## What would make RDR-001 decision-ready

- Full source audit with claims tied to `source_ledger.yaml`.
- A structured debate whose outputs update the matrices.
- At least one concrete minimal experiment comparing the same traces across
  package, code, PF, ContractSpec, StageGraph, SkillGraph, and compiled bridge.
- At least one inspected counterexample or negative result.
- Clear kill criteria for every hypothesis.
- Explicit separation between adopted claims and promising unsupported claims.

## What would kill the compiled-bridge hypothesis

- Package + tests + provenance performs as well as the bridge on the same
  traces with materially lower complexity.
- Runtime intervention cannot achieve acceptable activation precision.
- Evidence links do not improve debugging, admission, or rollback decisions.
- Verifier obligations are too weak or too expensive for the target traces.
- Security/admission can be handled by a simpler allowlist/quarantine model.
