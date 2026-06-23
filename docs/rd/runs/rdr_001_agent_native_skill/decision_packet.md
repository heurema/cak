# RDR-001 Decision Packet

Status: exploratory / not decision-ready

Research question:
What is a skill for an AI agent: text advice, workflow, executable code,
Program Function, ContractSpec, verifier, type transition, causal intervention,
or a hybrid package?

## Current supported claims

- Agent Skills package instructions, metadata, and optional resources and use
  them automatically when relevant (`src_anthropic_agent_skills_docs`).
- Progressive disclosure is a concrete packaging/loading pattern: metadata at
  startup, SKILL.md when triggered, resources/code as needed
  (`src_anthropic_agent_skills_docs`).
- Skill packages are a security and supply-chain surface; malicious skills can
  direct tool misuse, code execution, or data exfiltration
  (`src_anthropic_agent_skills_docs`).
- Voyager supports the hypothesis that executable external skill libraries can
  be reusable and compositional in stable environment-feedback settings
  (`src_voyager_arxiv`).
- AWM supports the hypothesis that workflow memories induced from trajectories
  can improve web-agent task performance (`src_awm_arxiv`).
- HMT challenges flat workflow memory by identifying workflow mismatch from
  entangled task logic and site-specific action details (`src_hmt_arxiv`).
- HASP supports the hypothesis that active Program Functions can provide
  runtime-control semantics beyond passive textual advice (`src_hasp_arxiv`).
- VASO supports the hypothesis that semantic contracts and verifier feedback
  can make some skill evolution proof-oriented rather than trace-only
  (`src_vaso_arxiv`).
- PSN supports the hypothesis that evolving skill libraries may need maturity
  gating, compositional structure, and rollback validation (`src_psn_arxiv`).

## Current unsupported claims

- "SkillPack should become a separate protocol now."
- "ContractSpec is the final CAK skill abstraction."
- "A skill is universally a Program Function."
- "A skill is universally executable code."
- "A skill is universally a workflow."
- "Package format solves runtime activation and intervention."
- "Self-verification is enough for admission."
- "Formal model checking is feasible for all CAK skill domains."
- "Seed research-process refs prove the quality of this run."
- "Skill supply-chain risk is fully understood."

## Open unknowns

- What is the minimum runtime hook model needed to compare passive and active
  skills?
- Which state variables are observable enough for typed-state retrieval and
  ContractSpec-style checking?
- How should CAK measure activation precision/recall for skills?
- How should CAK measure prevented failures rather than just post-hoc success?
- What security gate is mandatory before executable or active skills can run?
- How should conflicts between two active skills be detected and resolved?
- What is the authoring burden of hybrid packages with behavior, contracts,
  verifiers, tests, and telemetry?
- Which older planning/cognitive-architecture mechanisms transfer and which
  fail for LLM agents?

## Minimal experiment candidates

### Experiment A - Same traces, six skill forms

Take a small corpus of agent failure traces and encode the same repair as:

- text-only advice;
- workflow;
- executable script/code skill;
- HASP-style Program Function;
- ContractSpec/verifier obligation;
- hybrid package.

Measure task success, repair success, activation precision/recall, false
positive intervention, overblocking, auditability, latency/cost, and human
review burden.

### Experiment B - Retrieval mode comparison

For the same candidate skills, compare:

- semantic retrieval over descriptions;
- typed-state predicate matching;
- failure-signature routing;
- verifier-triggered retry.

Measure activation precision/recall and wrong-state application.

### Experiment C - Skill pollution simulation

Create broad, narrow, stale, conflicting, and malicious candidate skills. Run
admission gates in shadow mode:

- syntax/interface/mock execution;
- replay tests;
- counterexample tests;
- security review;
- utility threshold;
- quarantine and retirement.

Measure library pollution, conflict rate, review burden, and rollback success.

## Quality gate status

Current status: exploratory.

Research-ready blockers:

- Full-paper inspection is missing for the main papers.
- Implementation repos have not been inspected.
- Independent security analyses are missing.
- Research-process seed refs are not inspected.
- Older planning/cognitive-architecture sources are not inspected.
- Debate has not run.

Decision-ready blockers:

- No adversarial debate output yet.
- No source-ledger audit by an independent reviewer.
- No minimal experiment has been run.
- No counterexample source beyond HMT/security warnings has been inspected.
- Hypotheses have kill criteria but no measured results.

## Missing artifacts before decision-ready

- Completed debate with all roles in `debate.md`.
- Full-paper source-ledger entries for HASP, AWM, Voyager, VASO, PSN, and HMT.
- Implementation/repo inspections where available.
- At least one independent skill security or supply-chain analysis.
- At least one negative result or limitation source.
- Experiment protocol for same-trace comparison across skill forms.
- Quality gate pass recorded after evidence audit.

## Recommended next step

Run adversarial debate and evidence audit before drafting RDR-001.

After debate, update:

- `source_ledger.yaml`;
- `pattern_matrix.md`;
- `claim_matrix.md`;
- `hypothesis_matrix.md`;
- `adversarial_review.md`;
- this decision packet.

Only then decide whether RDR-001 is ready to be written.
