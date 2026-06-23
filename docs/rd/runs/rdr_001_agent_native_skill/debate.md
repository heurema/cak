# Structured Debate — RDR-001 Agent-Native Skill

Debate status: structured pass run on 2026-06-23

Execution mode: single-operator structured debate by Codex, not an independent
multi-agent debate. The roles below are analytic positions used to stress-test
the packet. They do not create new evidence.

Source boundary: only inspected `source_ledger.yaml` claims may support claims.
This debate can reframe, challenge, or prioritize claims, but it cannot promote
unsupported claims into evidence.

Decision boundary: this debate does not decide RDR-001, does not standardize a
skill format, and does not authorize runtime, schema, SkillPack, or ContractSpec
changes.

## Role outputs

| Role | Result | Artifact impact |
|---|---|---|
| Scout | The most important remaining leads are older planning/cognitive architecture sources, direct package+tests counterexamples, deeper security papers, and implementation-level runs of Voyager/SkillWiki/SkillJuror/security repos. | Keeps uninspected leads out of claims; informs `decision_packet.md` missing evidence. |
| Archivist | The current packet has enough source-ledgered claims for a research packet, but not enough implementation validation for a final RDR. C10 remains a low-confidence synthesis claim. | No new ledger claims from debate; reinforces `claim_matrix.md` boundaries. |
| Builder | H7 is still the most explanatory hypothesis because it accounts for package, runtime control, verifier, lifecycle, evidence, and security pressures in one model. Its minimal form is unknown. | Keep H7 as hypothesis; do not promote it to architecture. |
| Skeptic | The strongest alternative is Agent Skills-style package + tests + provenance + deny-by-default execution. It may be enough for v0.1/v0.2 and cheaper than a compiled bridge. | Add package+tests as the main counterexample to test. |
| Alienist | Non-obvious alternatives worth testing are admission-as-compiler, trace theorem, type-error handler, and causal intervention record. These are variants to compare, not new decisions. | Fold alternatives into trace corpus design rather than adding new standards. |
| Security reviewer | Skill packages mix instructions, code, resources, and tool authority. Cross-file and runtime-aware review is needed for untrusted executable/active skills, but the minimum admission gate is still unknown. | Security remains an experiment axis, not a completed design. |
| Evaluator | The next artifact should be a small CAK trace corpus proposal that makes hypotheses experimentally distinguishable without runtime/schema implementation in this PR. | Adds `trace_corpus_plan.md`; updates `decision_packet.md`. |
| Judge | The packet is stronger after evidence audit and structured debate, but it is still exploratory and not decision-ready. | Keep PR draft; do not write final RDR. |

## Motion A: Agent-native skill should be a compiled bridge between Evidence IR and Runtime IR.

Pro side:

- HASP supports active runtime intervention through executable PFs with
  `should_activate` and `intervene` (`claim_hasp_003`).
- VASO supports verifier-facing semantic contracts (`claim_vaso_002`).
- SkillRevise supports evidence-to-edit traces and preservation constraints
  (`claim_skillrevise_003`).
- SkillWiki/PSN support lifecycle/provenance/update pressure
  (`claim_skillwiki_repo_001`, `claim_psn_003`).
- Security sources show skill packages are hybrid prompt/code supply-chain
  objects (`claim_skillject_003`, `claim_malskillbench_002`).

Con side:

- A compiled bridge may be a unifying story that predicts too little.
- No inspected source proves a compiled bridge outperforms package + tests on
  the same CAK traces.
- The minimum Runtime IR and Evidence IR are unknown.
- The bridge may add fields before CAK proves which fields are load-bearing.

Debate result:

Keep H7 as the main hypothesis to test. Do not treat it as an architectural
claim. It becomes decision-relevant only if the same traces show that package,
PF, contract, stage memory, and lifecycle-only approaches fail to capture
behavior, safety, or auditability at lower complexity.

Artifact update required:

- Mark C10 as hypothesis-level synthesis in `decision_packet.md`.
- Add trace cases that test whether bridge fields are actually load-bearing.

## Motion B: Agent Skills-style package is enough for v0.1/v0.2 skill interoperability.

Pro side:

- Portable package structure, progressive disclosure, bundled resources, and
  tests may be sufficient for early interoperability.
- SkillJuror repo variants make package organization experimentally testable
  (`claim_skilljuror_repo_002`).
- A package + tests + provenance + deny-by-default policy may be simpler than
  compiling a separate runtime artifact.

Con side:

- Package validation is not activation, runtime admission, or verifier-gated
  control.
- HASP and VASO point to runtime/control and verifier obligations beyond a
  distribution shell (`claim_hasp_003`, `claim_vaso_002`).
- Security sources show package contents must be reviewed across instruction
  and artifact channels (`claim_skillject_003`).

Debate result:

Use Agent Skills-style package + tests as the baseline counterhypothesis. If it
matches richer forms on trace behavior, auditability, and safety with lower
complexity, it should kill or shrink the compiled-bridge hypothesis.

Artifact update required:

- Add trace-corpus rows where package + tests is a first-class comparison arm.

## Motion C: Program Functions are the best primitive for active skills.

Pro side:

- HASP gives the clearest inspected model of active skill control:
  `should_activate`, `intervene`, action override, context injection, and
  intervention logging (`claim_hasp_003`, `claim_hasp_004`).
- PFs are directly testable in shadow mode on recorded traces.

Con side:

- PFs can overblock correct behavior if activation predicates are imprecise.
- PFs do not by themselves solve package provenance, security admission,
  verifier obligations, or lifecycle governance.
- Active intervention can widen authority if effects and approval boundaries
  are not explicit.

Debate result:

PFs are the strongest candidate for active runtime skills, not the whole skill
definition. They should be tested as one representation under strict activation
precision and overblocking metrics.

Artifact update required:

- Add trace cases where PFs should fire, should not fire, and should only inject
  context rather than override action.

## Motion D: ContractSpec should remain separate from SkillSpec.

Pro side:

- VASO supports semantic contracts and counterexample-driven repair
  (`claim_vaso_002`, `claim_vaso_003`).
- Contract obligations can provide stronger verifier-facing evidence than
  free-form skill text.

Con side:

- VASO also shows that wrong proposition grounding can create false safety
  guarantees (`claim_vaso_004`).
- CAK may lack stable typed propositions for repository/filesystem/tool state.
- Collapsing ContractSpec into SkillSpec could prematurely mix proof, runtime,
  package, and lifecycle concerns.

Debate result:

Keep ContractSpec separate for now. Treat it as one verifier facet that may be
referenced by a skill candidate, not as the definition of skill.

Artifact update required:

- Add trace cases where a contract proves too little, proves the wrong thing,
  or catches a failure that package/tests miss.

## Motion E: StageGraph should replace linear workflow memory.

Pro side:

- HMT supports stage-level pre/postconditions and reports gains over flat memory
  in web settings (`claim_hmt_002`, `claim_hmt_003`).
- AWM reports workflow guidance can bias behavior in the wrong state
  (`claim_awm_004`), which stage checks are designed to reduce.

Con side:

- HMT still reports ambiguous grounding and subtle state-transition failures
  (`claim_hmt_004`).
- StageGraph depends on observable pre/postconditions.
- Early CAK workflows may be short enough for simpler workflow + retrieval +
  tests.

Debate result:

StageGraph is a strong candidate for web/workflow skills, but not a replacement
for all workflow memory. It should be tested only where state alignment and
observable stage predicates matter.

Artifact update required:

- Add trace cases for wrong-stage activation, unobservable preconditions, and
  dynamic UI/API drift.

## Motion F: SkillGraph lifecycle/governance is premature.

Pro side:

- If the skill set remains small, flat allowlist + quarantine may be cheaper
  than a lifecycle graph.
- A graph can become governance overhead before CAK has real skill volume.

Con side:

- PSN supports maturity-aware update gating and rollback pressure
  (`claim_psn_003`, `claim_psn_004`).
- SkillWiki repo supports provenance, lifecycle state, health, and repair
  vocabulary (`claim_skillwiki_repo_001`, `claim_skillwiki_repo_002`).
- Security and self-generated skill risks argue against an ungoverned flat
  registry for executable or active skills.

Debate result:

SkillGraph is premature as a required architecture, but lifecycle metadata is a
real experiment axis. The minimal comparison should be flat registry vs
quarantine vs lifecycle node under conflicting, stale, and self-generated skill
candidates.

Artifact update required:

- Add trace cases for library pollution, skill regression, stale skills, and
  rollback.

## Judge verdict

The debate strengthens the draft packet but does not make it decision-ready.

Current verdict:

- Research packet: yes.
- Final RDR: no.
- Architecture decision: no.
- Ready to merge as final research decision: no.
- Good draft to continue: yes.

Decision-grade blockers:

- No CAK trace corpus has been accepted or run.
- No same-trace comparison exists across package, PF, ContractSpec, StageGraph,
  SkillGraph, and compiled bridge.
- No direct package+tests counterexample has been validated.
- No implementation repos were run or reproduced.
- Older planning/cognitive architecture leads remain uninspected.
- Security/admission is not yet reduced to a minimal gate.

Next artifact:

- `trace_corpus_plan.md`, containing 5-10 proposed CAK failure traces and
  comparison arms for experiments A/B/C.
