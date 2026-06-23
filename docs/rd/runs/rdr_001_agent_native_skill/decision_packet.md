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
- Which proposed trace-corpus entries should be accepted?
- What benchmark/failure traces should be run after the corpus is selected?

## Quality gate status

Gate status: exploratory.

Target gate for this packet: research-ready, not decision-ready.

Decision-ready status: not decision-ready.

Using `docs/rd/research_quality_gate.md`, this run remains exploratory because:

- structured debate has been run as a single-operator structured pass, and a
  lightweight two-role Skeptic/Evaluator review has been run, but no full
  independent reviewer panel has accepted the trace corpus;
- minimal experiment is described but not implemented;
- counterevidence is incomplete;
- `trace_corpus_plan.md` proposes a corpus, but no CAK trace corpus has been
  accepted, written as fixtures, or run;
- implementation repositories were inspected only at README level and were not
  run or reproduced;
- top-six papers were inspected for targeted claims but not reproduced;
- full-paper/security audit beyond targeted sections is incomplete;
- older planning/cognitive architecture sources are uninspected leads;
- direct package+tests counterexample evidence was not found or validated;
- security/admission remains a research direction, not a complete design.

## Draft PR readiness gate

PR #10 can become ready for review as an exploratory research packet only after
`trace_corpus_plan.md` is judged sufficient for experiment design. That means:

- package + tests is treated as a serious baseline;
- every central hypothesis H1-H7 has at least one support path and one kill or
  weakening path;
- PF, ContractSpec, StageGraph, SkillGraph, and compiled-bridge traces have
  concrete scoring oracles;
- C10 remains marked as a hypothesis-level synthesis, not an architecture
  decision;
- the packet still avoids runtime, schema, SkillPack, ContractSpec, and final
  RDR changes.

Current readiness verdict: not ready.

The lightweight Skeptic/Evaluator review found that the trace plan is useful but
insufficient:

- T1-T8 are candidate scenarios, not accepted fixtures;
- scoring is not operationalized enough for pass/fail decisions;
- Experiment A and Experiment C do not yet have enough same-trace full-baseline
  coverage;
- T2 must be split into PF fire, no-fire/overblock, and
  context-injection-vs-override cases;
- T5 must be split into ContractSpec false-confidence and evidence/provenance
  diagnosis cases;
- T7 needs a flat registry + quarantine + regression-test counterexample before
  SkillGraph/lifecycle evidence is balanced;
- C10 / compiled bridge can only win if it beats package + tests + provenance +
  deny-by-default on the same traces at acceptable evidence cost.

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

Select 5-8 traces from `trace_corpus_plan.md`, write them as plain research
fixtures in a future docs/eval packet, and run same-trace comparisons before
drafting final RDR-001. Do not write final RDR-001 yet.
