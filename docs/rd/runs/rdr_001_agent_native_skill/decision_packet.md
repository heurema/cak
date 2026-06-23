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
- What benchmark/failure traces should be used?

## Quality gate status

Gate status: exploratory.

Target gate for this packet: research-ready, not decision-ready.

Decision-ready status: not decision-ready.

Using `docs/rd/research_quality_gate.md`, this run remains exploratory because:

- adversarial debate is planned but not run;
- minimal experiment is described but not implemented;
- counterevidence is incomplete;
- no CAK trace corpus exists for experiments A/B/C;
- implementation repositories were inspected only at README level and were not
  run or reproduced;
- top-six papers were inspected for targeted claims but not reproduced;
- full-paper/security audit beyond targeted sections is incomplete;
- older planning/cognitive architecture sources are uninspected leads;
- direct package+tests counterexample evidence was not found or validated;
- security/admission remains a research direction, not a complete design.

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

Run structured debate using the updated source ledger, then choose a minimal
CAK trace corpus for experiments A/B/C. Do not write final RDR-001 yet.
