# Pattern References for CAK R&D

This is not a dependency list.
This is not a required-tool list.
This is not an endorsed stack.
These references are inspected for reusable patterns that may inspire CAK R&D.

Seed references are not accepted evidence until inspected and recorded in a source ledger.

## How to use this file

Structure each reference as:

```markdown
## Reference name

Inspect for:
- ...

Why it matters:
- ...

Questions it informs:
- ...

Caution:
- ...

Potential CAK-native adaptation:
- ...

Evidence status:
- seed | inspected | source-ledgered | rejected
```

## Skill and procedural-memory anchors

### Voyager

Inspect for:

- executable code skills;
- external skill library without weight updates;
- self-verification before library admission;
- iterative prompting with environment feedback and execution errors;
- compositional reuse;
- transfer to new tasks / another agent benefiting from the skill library.

Why it matters:

- Voyager suggests that agent skills can be executable external artifacts, not
  model-weight updates.

Questions it informs:

- What is an agent-native skill?
- How should skill admission use execution evidence?
- When should skills remain external and auditable?

Caution:

- Stable API and clear environment feedback make Voyager easier than open web
  or enterprise tool governance.

Potential CAK-native adaptation:

- Skill artifact admission should require executable validation, verifier
  evidence, trace/replay, and compositional dependency tracking.

Evidence status:

- seed

### Agent Workflow Memory

Inspect for:

- workflow induction from trajectories;
- offline and online memory;
- abstract sub-routines;
- website/domain generalization;
- workflow action-space variant;
- brittleness in dynamic UI;
- need to diverge from workflow guidelines.

Why it matters:

- AWM shows workflow memory can improve web agents, but also shows why linear
  workflows and macro-actions are not enough.

Questions it informs:

- Should CAK represent workflows as lists, state machines, behavior trees, or
  guarded plans?
- How should retrieval account for runtime state?

Caution:

- Web workflows can break when UI state diverges from the learned routine.

Potential CAK-native adaptation:

- Represent workflows as guarded state machines or stage-aware plans with
  preconditions/postconditions, not fixed step lists.

Evidence status:

- seed

### HASP

Inspect for:

- Program Functions;
- should_activate / intervene interface;
- action override;
- context injection;
- structured intervention records;
- four intervention signals: timing, mode, correctness, outcome;
- executable validation;
- teacher review;
- strict filtering;
- library pollution risk.

Why it matters:

- HASP is a strong anchor for active runtime-control skills rather than passive
  prompt advice.

Questions it informs:

- When should a skill actively intervene?
- How should active skills be validated, recorded, and quarantined?

Caution:

- Active interventions can overblock, override valid behavior, or become unsafe
  without strong gates.

Potential CAK-native adaptation:

- Treat active skills as runtime control objects with hook semantics, audit
  records, rate limits, validation gates, and rollback/quarantine.

Evidence status:

- seed

### Agent Skills format

Inspect for:

- portable skill package ergonomics;
- SKILL.md-like metadata and instructions;
- scripts/references/assets separation;
- progressive disclosure;
- cross-agent reuse.

Why it matters:

- This is a baseline for portable skill packaging.

Questions it informs:

- Which package fields are distribution concerns?
- Which package fields need compiled runtime or verifier semantics?

Caution:

- Folder-based human-readable packages may not be enough for agent-native
  runtime control, verifier-gated admission, or safety.

Potential CAK-native adaptation:

- Use portable packaging only as a distribution layer; compile into CAK-native
  artifacts such as ContractSpec, SkillSpec, VerifierPlan, PolicySpec, and
  tests.

Evidence status:

- seed

### last30days-skill

Inspect for:

- horizon scanning;
- multi-source discovery;
- source scoring;
- entity-aware pre-research;
- cross-source cluster merging;
- grounded synthesis;
- shareable brief artifact generation;
- social/practitioner signal collection.

Why it matters:

- CAK R&D needs a discovery process richer than "ask one model."

Questions it informs:

- How should CAK run source discovery?
- How should a Scout separate leads from accepted evidence?

Caution:

- Social engagement is not truth. Discovery output must be audited through
  `source_ledger.yaml`.

Potential CAK-native adaptation:

- Horizon Scout role for research runs:
  discover sources, repos, discussions, and recent signals;
  extract candidate patterns;
  never convert discovery into accepted evidence without source ledger.

Evidence status:

- seed

### VASO

Inspect for:

- semantic skill contracts;
- formal/planner-facing interfaces;
- model-checker filtering;
- temporal safety specifications;
- counterexample traces used to improve skill contracts;
- frozen model weights with evolving external skill contracts.

Why it matters:

- VASO is close to CAK's ContractSpec/type-system direction.

Questions it informs:

- Should ContractSpec expose runtime predicates and verifier obligations?
- How should counterexample traces update contracts?

Caution:

- Formal interfaces may require assumptions that current agent environments do
  not expose cleanly.

Potential CAK-native adaptation:

- ContractSpec may need dual interfaces:
  runtime-facing predicates for the agent loop;
  verifier-facing formal obligations for safety or correctness.

Evidence status:

- seed

### Programmatic Skill Networks

Inspect for:

- executable symbolic skill programs;
- compositional skill networks;
- structured fault localization;
- maturity-aware update gating;
- rollback validation;
- structural refactoring.

Why it matters:

- PSN may offer better lifecycle semantics than a flat skill registry.

Questions it informs:

- Should CAK skills have dependency graphs, maturity levels, and rollback
  validation?

Caution:

- Symbolic networks may understate ambiguity in LLM agent state and tool
  environments.

Potential CAK-native adaptation:

- Skill libraries may need maturity levels, dependency graphs, refactoring
  operations, and rollback validation.

Evidence status:

- seed

### Hierarchical Memory Tree

Inspect for:

- decoupling logical planning from action execution;
- intent/stage/action hierarchy;
- observable preconditions and postconditions;
- stage-aware Planner/Actor split;
- preventing workflow mismatch across unseen websites.

Why it matters:

- HMT is highly relevant to CAK's state-conditioned retrieval and
  workflow-memory questions.

Questions it informs:

- How should CAK separate task intent, semantic stage, action grounding, and
  verifier conditions?

Caution:

- Website-specific grounding may not transfer without environment-specific
  selectors and postconditions.

Potential CAK-native adaptation:

- CAK memory should distinguish:
  task intent;
  semantic stage;
  action grounding;
  verifier conditions;
  environment-specific selectors.

Evidence status:

- seed

### SkillWiki

Inspect for:

- skill infrastructure;
- provenance-aware exploration;
- grounding reusable skills in originating evidence;
- continuous evolution of skill assets.

Why it matters:

- SkillWiki may be a closer analogue to a future SkillPack ecosystem than
  ordinary package managers.

Questions it informs:

- What provenance does a skill registry need?
- When should infrastructure follow runtime evidence rather than precede it?

Caution:

- Do not assume infrastructure/registry should come before runtime/verifier
  evidence.

Potential CAK-native adaptation:

- Treat provenance and continuous evolution as required metadata, but defer
  registry architecture until active runtime and verifier evidence exists.

Evidence status:

- seed

### SkillRevise

Inspect for:

- trace-conditioned skill revision;
- execution-grounded diagnosis;
- iterative skill repair;
- empirical utility measurement;
- cross-model transfer of revised skills.

Why it matters:

- SkillRevise may help CAK avoid one-shot skill authoring and instead revise
  skills through traces.

Questions it informs:

- How should CAK revise skill candidates after failed traces?
- Which utility metrics should gate revised skill admission?

Caution:

- Revision can overfit to recent traces or poison a shared library if admission
  gates are weak.

Potential CAK-native adaptation:

- Skill evolution should be trace-conditioned, versioned, verifier-gated, and
  empirically compared before admission.

Evidence status:

- seed

### Agent Skills security analyses

Inspect for:

- prompt injection through skill files;
- malicious skill classification;
- repository-context analysis;
- abandoned repository hijacking;
- approval widening / "don't ask again" hazards.

Why it matters:

- A skill ecosystem is also a supply-chain and prompt-injection surface.

Questions it informs:

- What trust metadata does a SkillPack need?
- How should CAK limit permission widening and self-poisoning?

Caution:

- Human-readable skills can be executable influence channels even when they are
  "just documentation."

Potential CAK-native adaptation:

- Every skill package needs trust metadata, provenance, sandboxing, permission
  declarations, exact-scope approvals, and quarantine/rollback.

Evidence status:

- seed

## Debate / multi-review / research-harness pattern references

### nitpicker

Inspect for:

- multiple independent reviewers;
- actor/critic debate;
- aggregator / meta-reviewer;
- reviewer agents with file/grep/git tools;
- transcript and trajectory logs;
- provider diversity;
- machine-readable output.

Why it matters:

- CAK R&D needs structured disagreement, not one-pass synthesis.

Questions it informs:

- Which debate roles and artifacts should CAK require?
- How should reviewers update source ledgers, pattern matrices, and unknowns?

Caution:

- A review harness can find disagreements without making the evidence true.

Potential CAK-native adaptation:

- R&D debate packet:
  Scout, Builder, Skeptic, Alienist, Security Reviewer, Evaluator, Judge.
  Judge cannot introduce unsupported claims.
  Every debate output must update source_ledger, pattern_matrix, or unknowns.

Evidence status:

- seed

### STORM-like systems

Inspect for:

- multi-perspective question asking;
- outline-first research;
- retrieval-grounded synthesis;
- citation discipline;
- article/survey generation from structured exploration.

Why it matters:

- Useful for research-plan and question-generation mechanics.

Questions it informs:

- How should CAK expand one research question into subquestions?
- Which source classes and perspectives are missing?

Caution:

- Do not assume article generation equals decision-grade architecture research.

Potential CAK-native adaptation:

- Use multi-perspective question generation before source discovery, then force
  all claims through source ledger and adversarial review.

Evidence status:

- seed

### AutoSurvey-like systems

Inspect for:

- paper search agents;
- topic mining and clustering;
- survey writer / quality evaluator split;
- citation coverage;
- multi-agent survey generation;
- structured quality evaluation.

Why it matters:

- Useful for literature synthesis and source coverage, especially for rapidly
  evolving agent-skill research.

Questions it informs:

- How should CAK separate source discovery, clustering, synthesis, and quality
  review?

Caution:

- Generated surveys can still miss negative results or implementation
  realities. Require source ledger and adversarial review.

Potential CAK-native adaptation:

- Use survey-style clustering to organize source discovery, but require
  implementation artifacts, negative evidence, and pattern transfer checks
  before decision-ready status.

Evidence status:

- seed

### SurveyG / citation-graph approaches

Inspect for:

- hierarchical citation graph;
- foundation/development/frontier layers;
- horizontal and vertical traversal;
- multi-agent validation.

Why it matters:

- Useful for avoiding flat bibliography lists and understanding research
  lineage.

Questions it informs:

- Which claims are foundation concepts, recent developments, or frontier claims?
- Where is counterevidence missing in the graph?

Caution:

- Citation structure can overvalue popular lineage and miss implementation
  failures.

Potential CAK-native adaptation:

- Research runs may maintain a reference graph:
  foundation concepts;
  recent developments;
  frontier claims;
  counterevidence.

Evidence status:

- seed

## Older planning / cognitive architecture references

### STRIPS / ADL / HTN

Inspect for:

- preconditions;
- postconditions;
- action languages;
- conditional effects;
- hierarchical decomposition.

Why it matters:

- These are human/AI planning ancestors of ContractSpec, workflow memory, and
  action schemas.

Questions it informs:

- Which planning abstractions transfer to agent runtime contracts?
- Where do explicit world-model assumptions break down?

Caution:

- Classical planning assumes more explicit world models than LLM agents usually
  have.

Potential CAK-native adaptation:

- Use preconditions, postconditions, and decomposition as reference patterns,
  but bind them to observable state, verifier checks, and failure traces.

Evidence status:

- seed

### Soar / production systems

Inspect for:

- procedural memory;
- working memory;
- if-then production rules;
- operator proposal/evaluation/application;
- chunking.

Why it matters:

- Useful historical analogue for agent-native procedural memory and runtime rule
  activation.

Questions it informs:

- What should CAK learn from production-rule activation without copying a whole
  cognitive architecture?

Caution:

- Do not copy cognitive architectures directly; extract mechanisms for runtime
  control and learning.

Potential CAK-native adaptation:

- Study production activation, operator selection, and chunking as mechanisms
  for state-conditioned skills and trace-grounded learning.

Evidence status:

- seed

## Pattern extraction rule

For every pattern reference, record:

```yaml
pattern:
source:
what to copy:
what not to copy:
agent-native adaptation:
risk:
evidence status:
```
