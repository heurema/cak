# RDR-001 Research Plan - What is an agent-native skill?

Status: exploratory
Target gate: research-ready, not decision-ready

## Research question

What is a skill for an AI agent: text advice, workflow, executable code,
Program Function, ContractSpec, verifier, type transition, causal intervention,
or a hybrid package?

## Why this matters

CAK needs a precise unit for reusable agent behavior before it can design
registries, protocols, runtime hooks, verifier gates, or experience-to-skill
compilation. If the unit is wrong, later surfaces such as SkillPack,
ContractSpec, SkillSpec, PolicySpec integration, replay, and admission control
will encode the wrong abstraction.

The human-software default is not safe to inherit blindly. Human developers use
documentation, packages, functions, macros, workflows, APIs, policies, and unit
tests with stable intent and explicit review. AI agents may ignore advice,
retrieve the right memory but apply it at the wrong time, call macros in invalid
states, fail to verify outcomes, or poison their own memory with bad lessons.

## Scope

- Compare text-only skills, workflow memories, executable code skills, Program
  Functions, semantic contracts, verifier-gated transitions, causal
  interventions, and hybrid packages.
- Extract reusable patterns from inspected sources into a source ledger,
  pattern matrix, claim matrix, and hypothesis matrix.
- Identify minimal experiments that could distinguish candidate skill
  definitions.
- Preserve ContractSpec as a hypothesis artifact, not as final architecture.
- Preserve SkillPack/protocol extraction as an open question.

## Non-goals

- Do not write the final RDR.
- Do not decide whether skills live inside CAK or in a separate SkillPack
  project.
- Do not implement runtime hooks, schemas, SkillPack, or verifier changes.
- Do not standardize a portable skill protocol.
- Do not treat seed references as evidence until inspected.
- Do not convert social/practitioner signal into truth.

## Human-software default to challenge

A human-software "skill" is often:

- documentation or training;
- a package;
- a function or macro;
- a workflow/runbook;
- a policy;
- a reusable test;
- an API wrapper.

For agents, each default can fail:

- documentation can be ignored or over-applied;
- packages can provide distribution without runtime control;
- functions can be called in invalid state;
- workflows can be brittle under partial observation or dynamic UI state;
- policies can block or allow without teaching repair;
- tests can sample behavior without proving safety;
- APIs can expose action surfaces without agent-state semantics.

## Seed sources

### Core skill/procedural-memory anchors

- HASP
- Agent Workflow Memory
- Voyager
- Agent Skills format

### Contract/type-system adjacent

- VASO
- Programmatic Skill Networks
- Hierarchical Memory Tree

### Research-process pattern refs

- last30days-skill
- nitpicker
- STORM-like systems
- AutoSurvey-like systems
- SurveyG / citation-graph approaches

### Security refs

- Agent Skills security / prompt-injection / supply-chain analyses

### Older planning/cognitive architecture

- STRIPS / ADL / HTN
- Soar / production systems

## Source classes to inspect

- Primary papers and abstracts for agent skills, workflow memory, and
  verification-guided skill evolution.
- Official product/spec documentation for portable Agent Skills formats.
- Implementation repositories where available.
- Security analyses of skill packages, prompt injection, and supply-chain
  attacks.
- Negative results and limitation sections.
- Older planning and cognitive-architecture references for pre/postconditions,
  hierarchical decomposition, and production-rule activation.
- Research-process systems for horizon scanning, multi-review, source ledgers,
  and citation-graph traversal.

## Search queries

- `"HASP" "Program Functions" "should_activate" "intervene"`
- `"Harnessing LLM Agents with Skill Programs"`
- `"Agent Workflow Memory" "workflow action" "WebArena"`
- `"Voyager" "skill library" "self-verification"`
- `"Agent Skills" "SKILL.md" "progressive disclosure" "security"`
- `"VASO" "semantic skill contracts" "model checker"`
- `"Programmatic Skill Networks" "maturity-aware update gating"`
- `"Hierarchical Memory Tree" "pre-conditions" "post-conditions"`
- `"agent skills" "prompt injection" "supply chain"`
- `"STRIPS" "ADL" "HTN" "preconditions" "postconditions"`
- `"Soar" "production systems" "chunking" "procedural memory"`
- `"STORM" "multi-perspective" "retrieval-grounded synthesis"`
- `"AutoSurvey" "citation coverage" "survey generation"`
- `"SurveyG" "citation graph" "multi-agent validation"`

## Exclusion criteria

- Exclude sources not inspected directly from claim support.
- Exclude social posts, launch threads, or engagement metrics as evidence for
  technical claims.
- Exclude claims that lack a concrete supporting passage and location.
- Exclude package-format claims from runtime-control conclusions unless a
  runtime mechanism is inspected.
- Exclude benchmark claims without noting environment assumptions and
  evaluation scope.
- Exclude architecture conclusions that would require an experiment not yet run.

## Expected counterarguments

- "A skill is just a package format." Counter: packaging may distribute
  instructions/resources without deciding activation, intervention, admission,
  or verification semantics.
- "A skill is executable code." Counter: code can be reusable but may lack
  state-conditioned activation, verifier evidence, security boundaries, or
  lifecycle controls.
- "A skill is a workflow." Counter: workflows help reuse experience but may
  fail when state diverges from the trace.
- "A skill is a contract." Counter: contracts may express obligations but not
  provide behavior, retrieval, repair, or telemetry.
- "One universal skill format is enough." Counter: different tasks may require
  passive guidance, active interventions, typed transitions, or hybrid packages.
- "If a source reports gains, adopt its representation." Counter: CAK must ask
  what transfers across agent loops, data classes, tools, and safety boundaries.

## Minimal experiment candidates

1. Same failure traces, six skill forms:
   text-only advice, workflow, executable script, Program Function,
   ContractSpec, and hybrid package.
2. Same skill package, three activation modes:
   semantic retrieval, typed-state predicate, and verifier-triggered routing.
3. Same invariant, four representations:
   PolicySpec, SkillSpec, ContractSpec, and VerifierPlan.
4. Shadow-mode active skills:
   compare proposed interventions against agent actions without applying them.
5. Skill pollution stress test:
   admit broad/narrow/conflicting skill candidates and measure false activation,
   overblocking, and retirement pressure.

## Stop/defer criteria

- Stop if inspected sources cannot support at least three materially different
  skill hypotheses.
- Defer if security and supply-chain evidence remains only a seed reference.
- Defer if no negative results or limitations are represented.
- Defer if all candidate experiments require runtime implementation beyond an
  implementation spike.
- Reject a candidate abstraction if it cannot define activation, evidence,
  failure mode, and rollback/admission behavior.
- Keep exploratory status until adversarial debate and evidence audit run.
