# RDR-001 Research Plan — What is an agent-native skill?

Status: exploratory

Target gate: research-ready, not decision-ready

## Research question

What is a skill for an AI agent?

Competing definitions to test:

- text advice;
- checklist;
- workflow;
- executable code;
- Program Function / runtime intervention;
- ContractSpec / type-error handler;
- verifier;
- type transition;
- causal intervention;
- StageGraph;
- SkillGraph node;
- portable package;
- compiled hybrid artifact.

The run should compare these definitions without deciding that any one is the
final CAK answer.

## Why this matters

Choosing the wrong unit of skill will distort:

- runtime hooks;
- SkillPack/protocol;
- ContractSpec;
- verifier plans;
- skill registry;
- memory compiler;
- security model;
- skill lifecycle;
- evaluation.

If CAK treats a skill as a package when the real unit is a state-conditioned
runtime transition, runtime design will be too weak. If CAK treats every skill
as executable code, it may miss procedural memory, verifier obligations,
admission evidence, and security envelopes.

## Current working hypothesis

“Agent-native skill = a compiled, governed bridge between evidence/provenance
and runtime control.”

This is only a hypothesis. It is inherited from
`docs/rd/03_skill_architecture_synthesis.md` as an input to test, not as an
architecture decision.

## Terminology guard

RDR-001's focal object is a Programmatic Runtime Skill: a reusable executable
behavior-control artifact that can observe current runtime state and proposed
action, decide whether it should activate, and modify, block, redirect, verify,
or repair the next agent transition.

Package-only systems are baselines and distribution references. Agent Skills /
SKILL.md packages, host plugin manifests, and script-backed folders are useful
for portability, resources, deterministic helpers, and host adapters, but they
do not by themselves establish runtime-control semantics.

Script-backed skills are not enough unless they are tied to a runtime
activation/intervention mechanism with a loop position, audit signal, admission
path, and lifecycle or quarantine story.

RDR-001 must not let Agent Skills packaging dominate the analysis. Use
`programmatic_runtime_skill_scope.md` to classify evidence before citing it for
Program Function-style or runtime-control claims.

## Scope

- agent skills and procedural memory;
- executable skills;
- workflow memory;
- contract/type-system skills;
- verifier-gated skills;
- package formats;
- skill lifecycle and repair;
- security/admission.

## Non-goals

- no runtime code;
- no schema changes;
- no final RDR decision;
- no SkillPack standardization;
- no ContractSpec promotion;
- no marketplace/registry design;
- no automatic skill generation implementation.

## Human-software default to challenge

Human software defaults include:

- packages;
- docs;
- functions;
- workflows;
- tests;
- plugins;
- policy files;
- registries.

These may not transfer to AI agents:

- agents may ignore text;
- agents may retrieve the right memory but apply it in the wrong state;
- agents may call macros in invalid states;
- authored skills may be prompt injection;
- package validation is not runtime admission;
- tests may not cover activation errors;
- self-generated skills can poison memory.

The research run should therefore ask whether a skill is the authored artifact,
the admitted runtime artifact, or the compiled bridge between them.

## Seed sources

Core:

- HASP — Harnessing LLM Agents with Skill Programs;
- Agent Workflow Memory;
- Voyager;

Contract/type-system adjacent:

- VASO — Formally Verifiable Self-Evolving Skills for Physical AI Agents;
- Programmatic Skill Networks / Evolving Programmatic Skill Networks;
- Hierarchical Memory Tree / Enhancing Web Agents with a Hierarchical Memory
  Tree;

Portable package / ecosystem:

- Agent Skills specification;
- SkillJuror;
- SkillReducer;
- SkillWiki;
- SkillRevise;

Security:

- Agent Skills prompt-injection / skill-injection papers;
- SkillJect or similar skill-based prompt injection work;
- malicious-or-not / repository-context skill classification work;
- stronger agent-skill security/supply-chain references found during source
  discovery;

Research-process / pattern refs:

- last30days-style horizon scanning;
- nitpicker-style multi-review/debate;
- STORM-like research systems;
- AutoSurvey-like systems;
- SurveyG / citation-graph approaches;

Older planning/cognitive architecture:

- STRIPS / ADL / HTN;
- Soar / production systems;
- production-rule systems / procedural memory where relevant.

For last30days and nitpicker, extract ideas/patterns only. Do not treat them as
dependencies or official tooling.

## Source classes to inspect

- papers;
- official specs;
- implementation repos;
- security analyses;
- benchmarks/evals;
- negative results;
- older planning/cognitive architecture;
- community/practitioner signals.

## Search queries

- “LLM agent executable skills Program Functions intervention”
- “agent skill library self verification executable code skills”
- “LLM agent workflow memory preconditions postconditions”
- “agent skills prompt injection supply chain”
- “agent skill package format SKILL.md”
- “LLM agent skill revision trace diagnosis preserve ledger”
- “programmatic skill networks maturity gating rollback”
- “formal verification semantic skill contracts LLM agents”
- “hierarchical memory tree web agents preconditions postconditions”
- “production systems procedural memory operator selection chunking”
- “HTN planning preconditions postconditions skills agents”

## Exclusion criteria

Exclude:

- sources that only mention “skills” as model capabilities without reusable
  artifacts;
- generic memory papers without procedural reuse;
- pure prompt engineering with no runtime/evidence mechanism;
- papers with no inspectable claims;
- tool repos without enough docs to extract patterns.

## Expected counterarguments

- “compiled bridge is overengineering”;
- “Agent Skills package is enough”;
- “Program Functions are enough”;
- “ContractSpec is enough”;
- “workflow memory is enough”;
- “security/admission can be deferred”;
- “source ledger makes research too heavy”;
- “one universal skill format is simpler”.

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

These are experiment sketches only. They do not authorize runtime or schema
implementation in this run.

## Stop/defer criteria

- not enough primary sources;
- no counterevidence found;
- no concrete implementation artifacts;
- claims cannot be source-ledgered;
- hypotheses cannot be experimentally distinguished.
