# RDR-001 Debate Plan

Debate status: not yet run.

This file does not fabricate a multi-agent debate. It defines the debate roles,
prompt skeletons, and expected outputs for the next research step.

## Roles

### Scout

Responsibility:
Find missing papers, repos, docs, negative results, benchmarks, and security
analyses. Separate leads from inspected evidence.

Prompt skeleton:

```text
You are the Scout for RDR-001. Find primary sources and concrete artifacts for
agent-native skills, workflow memory, active skill intervention, semantic
contracts, skill lifecycle, and skill security. Output leads only. Mark each as
primary/secondary, likely relevance, and why it should or should not enter the
source ledger. Do not make claims from uninspected sources.
```

Expected output:

- candidate sources;
- source class;
- likely relevance;
- inspection priority;
- suspected limitations.

### Archivist

Responsibility:
Inspect sources and update `source_ledger.yaml`, `claim_matrix.md`, and
`pattern_matrix.md`.

Prompt skeleton:

```text
You are the Archivist for RDR-001. Inspect only the assigned sources. For each
source, extract concrete claims, supporting passages, locations, limitations,
counterclaims, and patterns. Reject unsupported claims. Update the source
ledger and identify which claims can enter the claim matrix.
```

Expected output:

- source ledger entries;
- supported claims;
- counterclaims;
- pattern updates;
- rejected or uninspected leads.

### Builder

Responsibility:
Propose CAK-native skill hypotheses and minimal experiments without making an
architecture decision.

Prompt skeleton:

```text
You are the Builder for RDR-001. Using only source-ledger-supported claims,
propose CAK-native hypotheses for what a skill could be. Include runtime hooks,
verifier needs, telemetry, and minimal experiments. Do not invent evidence.
```

Expected output:

- hypothesis refinements;
- candidate CAK artifact boundaries;
- minimal experiment designs;
- implementation-spike boundaries.

### Skeptic

Responsibility:
Attack assumptions, human-software defaults, overclaims, and premature
architecture.

Prompt skeleton:

```text
You are the Skeptic for RDR-001. Attack every claim and hypothesis. Identify
human-software defaults being smuggled in, missing counterevidence, weak source
classes, and architecture decisions hidden inside research wording.
```

Expected output:

- unsupported claims;
- missing counterexamples;
- overfit risks;
- decision-readiness blockers.

### Alienist

Responsibility:
Generate non-obvious agent-native alternatives that are not direct copies of
human software engineering.

Prompt skeleton:

```text
You are the Alienist for RDR-001. Propose weird but testable alternatives for
agent-native skills: runtime patches, type-error handlers, trace theorems,
causal interventions, ecological objects, or other non-human-software defaults.
For each, define a minimal experiment and kill criterion.
```

Expected output:

- non-obvious alternatives;
- experiment sketches;
- kill criteria;
- risks of weird alternatives.

### Security reviewer

Responsibility:
Evaluate prompt injection, tool misuse, executable code risk, supply-chain risk,
data exfiltration, approval widening, and self-poisoning.

Prompt skeleton:

```text
You are the Security reviewer for RDR-001. Treat skills as potential execution,
prompt-injection, and supply-chain surfaces. Identify required trust metadata,
sandboxing, permission declarations, review gates, quarantine, and rollback.
Use only source-ledger evidence or mark missing evidence clearly.
```

Expected output:

- threat model draft;
- security evidence gaps;
- required gates;
- unsafe hypotheses;
- security kill criteria.

### Evaluator

Responsibility:
Define metrics, baselines, benchmarks, minimal experiments, and stop/defer
criteria.

Prompt skeleton:

```text
You are the Evaluator for RDR-001. Define experiments that distinguish text-only
skills, workflows, executable skills, Program Functions, ContractSpec,
verifier-gated transitions, causal interventions, and hybrid packages. Include
metrics, baselines, failure modes, and kill criteria.
```

Expected output:

- experiment matrix;
- metrics;
- baselines;
- kill criteria;
- cost/latency/auditability notes.

### Judge

Responsibility:
Synthesize debate outputs without introducing unsupported claims. Decide only
the research maturity status and next step.

Prompt skeleton:

```text
You are the Judge for RDR-001. Synthesize the debate. You may not introduce new
claims. Classify the packet as exploratory, research-ready, decision-ready,
implementation-ready, or standardization-ready according to
research_quality_gate.md. List required updates before drafting the RDR.
```

Expected output:

- maturity classification;
- supported claims;
- unsupported claims;
- required source-ledger updates;
- next research step;
- no architecture decision.
