# 00 — Project Thesis

Date: 2026-06-10

## One-sentence thesis

**CAK turns agent experience into typed, tested, replayable, policy-governed behavior.**

## Expanded thesis

The next layer of AI-agent infrastructure is not merely better prompting, more tools, or larger context windows. Production agents need a semantic substrate that can answer:

- What did the agent observe?
- What action did it propose?
- What effects could that action have?
- Which capabilities authorize the action?
- What evidence supports learned memory or a skill?
- What scope does the learned artifact apply to?
- Which verifier allowed or rejected the transition?
- Can the behavior be replayed?
- Can a bad skill or memory be quarantined, retracted, or unlearned?
- Can the same behavior run across model providers without silently changing semantics?

## Core framing

Existing systems mostly program execution:

```text
prompt + tools + workflow + memory + loop
```

CAK should program governed adaptation:

```text
observation → trace → evidence → effect → skill → verifier → promotion → replay → governance
```

## What CAK is not

CAK is not:

- a replacement for Python, TypeScript, or Rust;
- another prompt DSL;
- another agent chat framework;
- another model router;
- a Claude/OpenAI/Gemini-specific runtime.

## What CAK is

CAK is a typed semantic control layer for AI-agent behavior:

```text
CAK Spec       — human-facing declarations
CAK IR         — canonical typed artifacts
CAK Runtime    — guarded execution and replay
CAK Governance — verifier, promotion, audit, incident, unlearning
```
