# Decision Packet — RDR-001 Agent-Native Skill

Status: exploratory / not decision-ready

## Current supported claims

The current supported claims are exactly the claims listed in
`claim_matrix.md`:

- C1: Executable Program Functions provide stronger runtime control than
  prompt-only textual skills in HASP’s evaluated framing.
- C2: Workflow memories can improve web agents, but linear workflows/action
  macros can be brittle or bias behavior in dynamic environments.
- C3: Executable code skills with self-verification can compose and transfer in
  stable API environments.
- C4: Portable skill packaging is not the same as runtime control or
  verifier-gated admission.
- C5: Formal/semantic contracts become stronger when paired with
  verifier-facing obligations and counterexample traces.
- C6: Skill libraries likely require lifecycle metadata such as maturity,
  dependencies, rollback, and health to avoid flat-registry decay.
- C7: Stage-aware memory with pre/postconditions is a stronger candidate for web
  workflows than flat semantic retrieval.
- C8: Skill evolution requires diagnosis and preservation constraints to avoid
  overfitting and regression.
- C9: External skill packages create supply-chain and prompt-injection surfaces.
- C10: A compiled bridge between Evidence IR and Runtime IR may better explain
  the combined requirements than any single skill format.

Important: C10 is a hypothesis-level synthesis, not a supported architectural
decision. It is included to keep the main hypothesis testable, not to adopt the
compiled-bridge model.

The top-six paper anchors now have targeted full-paper inspection for the
listed claims. Voyager, SkillWiki, SkillJuror, Skill-Inject, and
prompt-injection agent-skills repositories have README-level implementation
inspection only.

## Current unsupported claims

- CAK should standardize SkillPack now.
- ContractSpec is the final skill abstraction.
- Program Functions are sufficient for all active skills.
- Agent Skills-style packaging is sufficient for runtime control.
- StageGraph should replace every workflow representation.
- SkillGraph governance is mandatory before any skill experiment.
- The compiled-bridge hypothesis is better than package + tests.
- Source-ledgered evidence audit is complete.
- Security/admission design is complete.
- Older planning/cognitive-architecture references support the current
  hypothesis.
- Package + tests is sufficient for CAK skill interoperability.
- README-level repository inspection is enough to validate implementation
  behavior.

## Open unknowns

- Is compiled bridge too complex?
- Can a simpler package + tests approach work?
- What is the minimal Runtime IR?
- What is the minimal Evidence IR?
- How much security/admission is necessary before runtime use?
- Can ContractSpec, PFs, and StageGraph share one activation model?
- How should the accepted trace fixtures be written without creating a schema
  decision?
- What benchmark/failure traces should be run after fixtures are authored?

## Quality gate status

Gate status: exploratory.

Target gate for this packet: research-ready, not decision-ready.

Decision-ready status: not decision-ready.

Using `docs/rd/research_quality_gate.md`, this run remains exploratory because:

- structured debate has been run as a single-operator structured pass, and a
  lightweight two-role Skeptic/Evaluator review has been run, but no full
  independent reviewer panel has reviewed the accepted fixture plan;
- minimal experiment is described but not implemented;
- counterevidence is incomplete;
- `trace_corpus_plan.md` now accepts a research-fixture plan, but the fixtures
  have not been written as separate eval artifacts or run;
- implementation repositories were inspected only at README level and were not
  run or reproduced;
- top-six papers were inspected for targeted claims but not reproduced;
- full-paper/security audit beyond targeted sections is incomplete;
- older planning/cognitive architecture sources are uninspected leads;
- direct package+tests counterexample evidence was not found or validated;
- security/admission remains a research direction, not a complete design.

## Trace corpus plan sufficiency

Trace corpus plan sufficiency: pass.

Experiment evidence sufficiency: fail.

The pass is narrow: `trace_corpus_plan.md` now contains an accepted
research-fixture plan with eight traces and the requested minimum fixture shape.
It does not mean any experiment has run, and it does not make RDR-001
decision-ready.

The accepted trace set is:

- T1: wrong-state package activation;
- T2a: PF should fire on a labeled failure;
- T2b: PF should not fire on a near-match control;
- T2c: PF context injection vs action override;
- T5a: ContractSpec false confidence from bad grounding;
- T5b: evidence/provenance diagnosis after grounding failure;
- T6: workflow brittleness with package + tests and compiled bridge arms;
- T7: lifecycle governance vs flat quarantine counterexample.

The sufficiency pass means:

- package + tests is treated as a serious baseline;
- T2 has been split into fire, no-fire/overblock, and
  context-injection-vs-override cases;
- T5 has been split into false-confidence and evidence/provenance diagnosis
  cases;
- T6 includes package + tests and compiled bridge arms;
- T7 includes a flat registry + quarantine + regression-test counterexample;
- every accepted trace has the requested minimum fixture fields;
- PF, ContractSpec, StageGraph, SkillGraph, and compiled-bridge traces have
  scoring oracles and kill/defer signals;
- C10 remains marked as a hypothesis-level synthesis, not an architecture
  decision;
- the packet still avoids runtime, schema, SkillPack, ContractSpec, and final
  RDR changes.

Remaining blockers before decision-ready status:

- fixtures are not implemented as separate research/eval artifacts;
- no same-trace comparison has been run;
- no quantitative result exists for package + tests vs PF vs ContractSpec vs
  StageGraph vs SkillGraph vs compiled bridge;
- no human has chosen adopt, reject, defer, or prototype deeper.

## Minimal experiment candidates

Experiment A: same failure traces, multiple representations:

- Agent Skills-style package;
- ContractSpec;
- Program Function;
- StageGraph/HMT-like memory;
- SkillGraph node;
- compiled hybrid artifact.

Experiment B: same skill package imported under different admission gates:

- no admission;
- static validation only;
- verifier-gated;
- replay/shadow-gated;
- security+provenance gated.

Experiment C: same workflow encoded as:

- linear workflow;
- state machine;
- StageGraph;
- Program Function;
- ContractSpec + repair handler.

## Recommended next step

Write the eight accepted traces from `trace_corpus_plan.md` as plain research
fixtures in a future docs/eval packet, then run same-trace comparisons before
drafting final RDR-001. Do not write final RDR-001 yet.
