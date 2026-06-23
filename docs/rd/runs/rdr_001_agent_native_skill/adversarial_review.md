# RDR-001 Adversarial Review

Status: first adversarial review

This review attacks the current research packet. It does not decide the RDR.

## Attack: one universal skill format

The packet still risks looking for one master abstraction. The inspected
sources point in different directions:

- Agent Skills: packaging and progressive disclosure.
- Voyager/PSN: executable external artifacts.
- AWM/HMT: workflow or structured memory.
- HASP: active runtime intervention.
- VASO: semantic contracts and verifier-facing obligations.

Those may be facets, not one object. A premature "SkillSpec" could flatten
different mechanisms into one leaky schema.

## Attack: overfitting to HASP / Program Functions

HASP is currently the strongest source for active runtime skills, but this run
only inspected the abstract. It is not enough to adopt PFs as the CAK primitive.
PF-style `should_activate` / `intervene` may work for some failure-prone states
and fail badly when state observability is weak. Active interventions also need
false-positive measurement, permission boundaries, and stop conditions.

## Attack: overfitting to Voyager / code skills

Voyager makes executable code skills compelling, but Minecraft provides stable
feedback loops and an environment API unlike many CAK target settings. Code
skills do not automatically solve activation, authorization, supply-chain risk,
or verifier admission. Treating "skill = code" would ignore passive guidance,
contracts, and state-conditioned intervention.

## Attack: overfitting to AWM / workflows

AWM supports workflow memory as a useful pattern, but HMT directly warns about
flat memory causing workflow mismatch across unseen websites. Workflow skills
without typed state, stage validation, and repair exits can become brittle
macros. A workflow may be an ingredient, not the skill unit.

## Attack: premature SkillPack/protocol extraction

The packet has not shown two independent runtime adapters or conformance tests.
Agent Skills documentation proves that a package format can be useful, but it
also documents cross-surface differences in runtime and network semantics.
Therefore a portable CAK SkillPack would be premature. At this stage, CAK should
study package facets and runtime hooks without extracting a protocol.

## Attack: package format does not solve runtime control

Packaging instructions, scripts, and resources is not the same as deciding:

- when a skill activates;
- whether it can override actions;
- which permissions it has;
- how verifier evidence is checked;
- how it is quarantined or retired;
- how conflict with another skill is resolved.

Any RDR that says "skill = package" without runtime semantics would be weak.

## Attack: skill supply-chain risk is underdeveloped

The Anthropic Agent Skills docs explicitly warn that malicious Skills can cause
tool misuse, code execution, and data exfiltration. This packet lacks broader
independent security analyses of prompt injection, skill dependency hijacking,
plugin marketplace trust, abandoned repositories, and approval widening. That
gap blocks decision-ready status for any active or executable skill design.

## Attack: model-generated source claims

The current claim matrix is mostly grounded in inspected abstracts and one
official docs page. That is acceptable for exploratory status, but not for a
decision. Abstracts are author claims, not full evidence. The next pass must
inspect full papers, implementations, benchmarks, and limitations. Seed refs
such as last30days-skill, nitpicker, STORM-like systems, AutoSurvey-like
systems, SurveyG, STRIPS/ADL/HTN, and Soar remain leads only.

## Attack: research-run bureaucracy

The packet has many artifacts. That can become process theater if the artifacts
do not reject weak claims. The quality gate must be used to say "not ready" and
to narrow the next experiment. If the packet just gives a RDR author more prose,
it fails.

## Missing evidence

- Full-paper inspection for HASP, AWM, Voyager, VASO, PSN, and HMT.
- Implementation repos and runnable artifacts, especially for Voyager, HASP,
  PSN, and HMT.
- Independent security analyses of skills as prompt-injection and supply-chain
  surfaces.
- Negative results for active skills, workflow memory, executable skills, and
  contract-heavy skill definitions.
- Older planning/cognitive-architecture sources: STRIPS/ADL/HTN and Soar are
  not inspected.
- Research-process systems: last30days-skill, nitpicker, STORM-like,
  AutoSurvey-like, and SurveyG are not inspected.

## Missing counterexamples

- A text-only skill that beats active intervention because runtime state is too
  ambiguous.
- An executable skill that passes tests but performs harmful external action.
- A workflow memory that activates on a semantically similar but invalid state.
- A ContractSpec that is correct but too expensive or too narrow to author.
- Two active skills that conflict and each looks locally valid.
- A skill package whose metadata is safe but referenced resources are malicious.

## Questions for debate

- Should RDR-001 define one skill abstraction or a taxonomy of skill facets?
- Is active intervention the core of an agent-native skill, or just one mode?
- Is ContractSpec a skill facet, a sibling artifact, or a verifier obligation?
- What is the minimal runtime hook set needed to test H2 without building a
  SkillPack?
- What security gate is mandatory before executable or active skills can run?
- Which hypothesis can be killed fastest with a small experiment?

## What would make RDR-001 decision-ready?

- Full-paper and implementation inspection for the primary sources.
- At least one independent security analysis in the ledger.
- At least one negative result or counterexample source.
- A completed debate with Scout, Archivist, Builder, Skeptic, Alienist,
  Security reviewer, Evaluator, and Judge.
- A minimal experiment that compares at least text-only, workflow, executable,
  Program Function, ContractSpec, and hybrid skill forms on the same traces.
- Explicit kill criteria for each hypothesis.
- A decision packet that names which claims are unsupported and refuses to make
  architecture decisions from seed references.
