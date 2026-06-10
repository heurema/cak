# 10 — Roadmap

## Full-solution milestones

| Milestone | Full-solution scope | Success criteria | MVP slice |
|---|---|---|---|
| Semantic core | CAK IR schema, parser/resolver, effect lattice, Scope, EvidenceSpec | TaskCapsule compiles, typechecks, and lowers to one backend | CAK IR core + TaskCapsule compiler |
| Safe execution | Agent VM, verifier, policy engine, Sandbox/SimSpec, trace store | Medium-risk tasks run with checks, approvals, replay traces | Agent VM + simple verifier |
| Learning pipeline | Memory/Skill/Effect compilers, contradiction manager, registry | Traces produce candidates; promotions need evidence and shadow eval | Memory/effect/skill candidates |
| Portability and cost | Provider layer, fallback graphs, CostGuard, ContextCache | Same TaskCapsule runs on two providers with cost envelope | Provider skeleton + CostGuard |
| Governed scale-out | Domain packs, incidents, review queues, trust tiers | Teams publish, approve, quarantine, and unlearn artifacts | Registry + review queue |

## First artifacts to build

1. CAK IR core schema.
2. TaskCapsule compiler.
3. Agent VM prototype.
4. EvidenceSpec.
5. Simple verifier.
6. Frontier adapter skeleton.
7. Trust inspector.
8. Replay harness.

## Suggested first wedge

Start as:

```text
Replay + Effect/Capability Governance for tool-using agents
```

Architect as:

```text
Agent Learning IR with trace-to-skill evolution
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
