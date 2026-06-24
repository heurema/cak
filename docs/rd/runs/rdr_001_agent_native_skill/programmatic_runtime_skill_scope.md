# Programmatic Runtime Skill Scope Gate

Status:
exploratory guardrail for RDR-001

## Why this file exists

CAK must not confuse ordinary skill packages with runtime-control skills.
Agent Skills / SKILL.md packages are useful for distribution. Script-backed
skills are useful for deterministic helpers. Host plugins and manifests can
adapt a skill package to a particular environment.

Those are not the same thing as Program Function skills or active
runtime-control skills. A package can carry instructions, scripts, resources,
and metadata without giving CAK an activation predicate, a loop position, or
authority over the next agent transition.

This gate exists so RDR-001 does not count package-only, script-only, or
plugin-only examples as evidence for programmatic runtime skills.

## Working definition

Programmatic Runtime Skill:

A reusable executable behavior-control artifact that can observe or match the
agent's current runtime state and proposed action, decide whether it should
activate, and then modify, block, redirect, verify, or repair the agent's next
transition.

Required properties:

- activation predicate;
- access to runtime state;
- access to proposed action or transition context;
- explicit loop position;
- executable intervention behavior;
- audit/intervention record;
- verifier or outcome signal;
- admission / validation path;
- lifecycle or quarantine story.

## In scope

- HASP-style Program Functions;
- `should_activate` / `intervene` modules;
- `before_action` / `after_action` hooks that can modify, block, or route
  repair;
- ContractSpec / type-error handlers when they can block or route runtime
  transitions;
- verifier-triggered repair loops;
- state-machine / StageGraph runtimes with observable pre/postconditions;
- action override / context injection frameworks;
- policy patch systems;
- runtime guardrails that operate on proposed actions, not only final text.

## Out of scope for "programmatic runtime skill" claims

- plain Agent Skills packages;
- SKILL.md only;
- `scripts/` folders without runtime activation;
- document/PDF/DOCX/XLSX skills;
- ordinary plugin manifests;
- tool wrappers;
- prompt libraries;
- workflow markdown;
- examples that require the model to remember to call the script;
- static linting tools with no agent-loop position.

Out-of-scope does not mean useless. It means these artifacts are distribution,
packaging, adapter, or helper references, not evidence for runtime-control
skills.

## Classification checklist

- has_activation_predicate: yes/no
- sees_runtime_state: yes/no
- sees_proposed_action: yes/no
- runtime_position: before_action | after_action | verifier | planner |
  prompt_only | unknown
- can_modify_action: yes/no
- can_block_action: yes/no
- can_inject_context: yes/no
- can_route_repair: yes/no
- emits_intervention_record: yes/no
- has_verifier_signal: yes/no
- has_admission_validation: yes/no
- has_rate_limits_or_anti_oscillation: yes/no
- has_lifecycle_or_quarantine: yes/no

Verdicts:

true_pf_like:
  satisfies activation + state/action + runtime position + intervention.

partial:
  satisfies some runtime/control properties but lacks full PF interface.

packaging_only:
  useful distribution reference, not runtime skill evidence.

not_relevant:
  generic scripts/tools/docs.

## How to use this gate in RDR-001

- Do not count package-only systems as support for Programmatic Runtime Skill.
- Do not cite Agent Skills examples as evidence that runtime-control skills
  exist.
- Do not count scripts as programmatic runtime skills unless they are invoked by
  a runtime activation/intervention mechanism.
- Keep Agent Skills/Codex/Claude plugin references in distribution/adapters
  sections only.
- Keep HASP as the main positive anchor for Program Function semantics.
- Keep AWM as workflow-memory baseline.
- Keep Voyager as executable-code-skill baseline.
- Keep VASO/ContractSpec as proof-carrying contract line.
- Keep HMT as state/stage memory line.

## Search strategy for future evidence audit

Search queries:

- "LLM agent Program Function should_activate intervene"
- "state action intervention function LLM agent"
- "agent runtime hook action override context injection"
- "executable guardrails agent loop intervention"
- "LLM agent policy patch runtime intervention"
- "verifier triggered repair loop agent"
- "agent contract handler proposed action block repair"
- "LLM agent before_action hook modify action"
- "runtime skill library action modification"
- "policy patch library LLM agent"
- "agent harness intervention functions"

Exclusion queries:

- exclude "SKILL.md"
- exclude "document skill"
- exclude "PDF skill"
- exclude "prompt library"
- exclude "plugin only"

Use the exclusion queries unless specifically studying distribution,
packaging, or host adapters.

## Consequences

RDR-001 can still compare package skills, workflows, executable code skills,
Program Functions, ContractSpecs, StageGraphs, SkillGraphs, and compiled bridge
artifacts.

The primary CAK target is now narrowed:

CAK is looking for agent-native runtime-control skills, not merely
host-compatible skill packages.
