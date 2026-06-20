# CAK R&D Charter

## Mission

CAK R&D studies how AI agents should accumulate, verify, execute, and revise
experience. The goal is not to copy human software abstractions blindly, but to
discover agent-native forms of programming, memory, skills, and governance.

## Why R&D before more implementation

The ContractSpec MVP is useful because it makes one concrete hypothesis
executable: some behavior constraints may be better expressed as typed
contracts than as passive instructions or broad policies. It should not
prematurely define the whole CAK architecture. A working checker can prove that
one shape is possible without proving that it is the right unit for skills,
protocols, verifier hooks, or runtime governance.

Skill systems need runtime semantics, verifier semantics, security boundaries,
retrieval semantics, and lifecycle controls. A skill that works as a document
may fail as a runtime control object. A skill that works inside one agent loop
may be unsafe or meaningless when moved to another loop. A skill that improves
one trace can pollute a lifelong library if admission, replay, retirement, and
conflict handling are weak.

A protocol without a proven runtime risks becoming YAML-only ideology: a neat
shape that describes intent but does not change agent behavior when the agent is
confused, distracted, adversarially prompted, or in the wrong state. A runtime
without portable boundaries risks becoming a monolith: useful locally, but hard
to audit, hard to adapt, and impossible to standardize.

## Core rule

Research before architecture.
Architecture before implementation.
Implementation before standardization.
Standardization only after multiple runtimes or conformance experiments.

## Agent-native design posture

- Human-software defaults are hypotheses, not defaults.
- Every major design must include "why the human default may fail for agents."
- Prefer state-conditioned runtime mechanisms over passive prompt advice when reliability matters.
- Prefer verifier-gated artifacts over self-asserted confidence.
- Prefer trace/replay/evidence-backed learning over ungrounded memory writes.
- Treat skill evolution as dangerous until filtered, tested, replayed, and measured.
- Separate "authoring a skill" from "admitting a skill into an active runtime."
- Do not standardize a protocol until at least two independent runtime adapters or conformance tests exist.

## R&D workflow

1. Research question
2. Human-default baseline
3. Why human default may fail for agents
4. Existing literature and systems
5. CAK-native hypothesis
6. Weird / non-obvious alternatives
7. Minimal experiment
8. Evaluation criteria
9. Kill criteria
10. Decision
11. Implementation candidate, if any

## Implementation freeze rule

New major runtime features should link to one of these:

- an RDR;
- a small experiment;
- an explicit "implementation spike" label.

Small bug fixes, CI, docs cleanup, and existing-scope tests do not require an
RDR. The rule applies to major architecture choices: new runtime surfaces,
protocol boundaries, skill admission mechanisms, memory-write paths, verifier
interfaces, extraction decisions, and standardization claims.

## Current research posture

- ContractSpec is experimental.
- SkillPack/protocol is open.
- CAK remains the reference runtime for now.
- Separate project extraction is deferred until evidence supports it.
