# 10 — Roadmap

## v0.1 first

The first shipped slice should be:

```text
MCP gateway/proxy + tool-boundary governance + trace for one class of agent
```

The initial target is a SaaS or operations agent with a small set of governed
tools. v0.1 should prove action classification, capability checks, policy
decisions, gateway enforcement, and trace explanation before learning or
portability work.

## v0.1 artifacts

1. Action proposal format.
2. EffectSpec for governed tool calls.
3. Capability manifest bound to real tool identity.
4. PolicySpec with a chosen predicate language.
5. Credential-owning MCP gateway/proxy.
6. Pre-execution verifier.
7. Trace schema and recorder.
8. Semantic replay harness for recorded tool calls.
9. One integration example with an existing MCP-capable agent stack.
10. Baseline comparison against trace-only plus existing policy engine.

## Full-solution milestones

| Milestone | Full-solution scope | Success criteria | MVP slice |
|---|---|---|---|
| Semantic core | CAK IR schema, parser/resolver, effect lattice, Scope, EvidenceSpec | TaskCapsule compiles, typechecks, and lowers to one backend | Action/Effect/Policy subset |
| Safe execution | Agent VM, verifier, policy engine, Sandbox/SimSpec, trace store | Medium-risk tasks run with checks, approvals, replay traces | Tool gateway + pre-exec verifier |
| Learning pipeline | Memory/Skill/Effect compilers, contradiction manager, registry | Traces produce candidates; promotions need evidence and shadow eval | Deferred until tool-boundary proof |
| Portability and cost | Provider layer, fallback graphs, CostGuard, ContextCache | Same TaskCapsule runs on two providers with cost envelope | Deferred until one-provider success |
| Governed scale-out | Domain packs, incidents, review queues, trust tiers | Teams publish, approve, quarantine, and unlearn artifacts | Deferred until real artifact volume |

## First artifacts to build

1. v0.1 Action/Effect/Policy schemas.
2. MCP gateway/proxy prototype.
3. Simple verifier.
4. Trace schema.
5. Semantic replay harness.
6. Grounding/EnvSpec note for the first tool family.
7. Baseline comparison harness.

## Suggested first wedge

Start as:

```text
Effect/Capability Governance for tool-using agents
```

Architect as:

```text
Tool-boundary governance with trace, then evidence-backed learning
```

Preferred first domain:

```text
SaaS / operations tools before coding agents
```

## Avoid early

- Full general-purpose programming language.
- Visual builder.
- Marketplace.
- Free-form swarm orchestration.
- Provider-specific canonical artifacts.
- Model fine-tuning loop.
- Browser-only agent system.
- Prompt DSL.
- Automatic trace-to-skill learning before v0.1 enforcement works.
