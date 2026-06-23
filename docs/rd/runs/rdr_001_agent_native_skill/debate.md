# Debate Plan — RDR-001 Agent-Native Skill

Debate status: not yet run

This file does not fabricate a real multi-agent debate. It defines the debate
to run after evidence audit.

## Roles

| Role | Responsibility | Prompt skeleton | Expected output | Artifact updated |
|---|---|---|---|---|
| Scout | Find missing papers, repos, docs, security analyses, benchmarks, negative results, and older planning/cognitive-architecture sources. | "Find candidate sources for RDR-001. Output leads only. Mark primary/secondary, source class, relevance, and inspection priority. Do not make claims from uninspected sources." | Lead list with inspection priority and suspected limitations. | `source_ledger.yaml` leads |
| Archivist | Inspect assigned sources and extract claims, passages, limitations, counterclaims, and patterns. | "Inspect only assigned sources. Extract claims with supporting passages and locations. Reject unsupported claims. Distinguish inspected sources from leads." | Source ledger entries, supported claims, rejected claims. | `source_ledger.yaml`, `claim_matrix.md`, `pattern_matrix.md` |
| Builder | Propose CAK-native hypotheses and minimal experiments without deciding architecture. | "Using only source-ledgered claims, refine hypotheses for what a skill could be. Include runtime hooks, verifier needs, telemetry, and minimal experiments." | Hypothesis refinements and experiment sketches. | `hypothesis_matrix.md`, `decision_packet.md` |
| Skeptic | Attack assumptions, human-software defaults, overclaims, and premature decisions. | "Attack every claim and hypothesis. Identify weak evidence, missing counterexamples, hidden architecture decisions, and premature standardization." | Objections, blockers, missing counterevidence. | `adversarial_review.md`, `decision_packet.md` |
| Alienist | Generate non-obvious agent-native alternatives. | "Propose weird but testable alternatives: runtime patches, type-error handlers, trace theorems, causal interventions, ecological objects. For each, define experiment and kill criterion." | Alternative hypotheses and kill criteria. | `hypothesis_matrix.md` |
| Security reviewer | Evaluate prompt injection, tool misuse, executable code, supply chain, data exfiltration, approval widening, and self-poisoning. | "Treat skills as execution, prompt-injection, and supply-chain surfaces. Identify required trust metadata, sandboxing, permission declarations, review gates, quarantine, and rollback." | Threat model notes, required gates, unsafe hypotheses. | `source_ledger.yaml`, `pattern_matrix.md`, `decision_packet.md` |
| Evaluator | Define metrics, baselines, benchmarks, minimal experiments, and stop/defer criteria. | "Design experiments that distinguish text-only skills, workflows, executable skills, PFs, ContractSpec, verifier-gated transitions, causal interventions, and hybrids." | Experiment matrix, metrics, baselines, kill criteria. | `research_plan.md`, `hypothesis_matrix.md`, `decision_packet.md` |
| Judge | Synthesize debate without adding unsupported claims. | "Classify maturity using `research_quality_gate.md`. Do not introduce new claims. List required updates before final RDR." | Maturity verdict, supported/unsupported claims, next step. | `decision_packet.md` |

## Debate motions

| Motion | Pro side | Con side | Required evidence | Possible experiment |
|---|---|---|---|---|
| Motion A: “Agent-native skill should be a compiled bridge between Evidence IR and Runtime IR.” | Builder, Security reviewer | Skeptic, Alienist | Source-ledgered evidence that package, code, PF, contract, memory, lifecycle, and security needs cannot be captured by one simpler primitive. | Same traces represented as package, PF, ContractSpec, StageGraph, SkillGraph node, and compiled hybrid. |
| Motion B: “Agent Skills-style package is enough for v0.1/v0.2 skill interoperability.” | Scout, Builder | Security reviewer, Skeptic | Agent Skills docs, SkillJuror, SkillReducer, security papers, and evidence about package/runtime gaps. | Same package under no admission, static validation, verifier-gated, replay-gated, and security+provenance gates. |
| Motion C: “Program Functions are the best primitive for active skills.” | Builder, Evaluator | Skeptic, Security reviewer | HASP details, activation precision evidence, false-positive/overblocking data, permission model. | Shadow-mode PF intervention on recorded traces. |
| Motion D: “ContractSpec should remain separate from SkillSpec.” | Skeptic, Security reviewer | Builder | VASO details, CAK state observability, grounding failures, verifier value. | Encode one invariant as SkillSpec, ContractSpec, PF, and verifier plan. |
| Motion E: “StageGraph should replace linear workflow memory.” | Builder, Evaluator | Skeptic | AWM/HMT full-paper evidence, web-agent mismatch traces, pre/postcondition observability. | Same workflow encoded as linear workflow, state machine, StageGraph, PF, and ContractSpec + repair handler. |
| Motion F: “SkillGraph lifecycle/governance is premature.” | Skeptic, Scout | Builder, Security reviewer | Skill library pollution evidence, PSN/SkillWiki details, security/lifecycle data, CAK skill-volume assumptions. | Simulate flat registry vs quarantine vs lifecycle graph under broad/narrow/conflicting candidates. |
