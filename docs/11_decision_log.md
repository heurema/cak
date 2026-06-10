# 11 — Decision Log

| Date | Project | Decision | Reason | What this prevents | Review date |
|---|---|---|---|---|---|
| 2026-06-10 | CAK | Build CAK as declarative surface + canonical CAK IR + governed runtime, not as full general-purpose language | Strongest moat is typed learning artifacts, replay, governance, and portability | Parser/tooling ecosystem wars; another prompt DSL or agent shell | After CAK IR v0.1 and first replayable TaskCapsule demo |
| 2026-06-10 | CAK | Make artifact lifecycle the core product spine | Production pain is uncontrolled agent action, learning, cost, vendor dependency, and audit gaps | Over-focusing on syntax or abstract research | 2026-06-17 |
| 2026-06-10 | CAK | Use provider-native features only as acceleration targets | Prevents hard vendor lock while exploiting frontier capabilities | Claude/OpenAI/Gemini-specific semantics becoming source of truth | 2026-06-24 |
| 2026-06-10 | CAK | Treat EvidenceSpec and ScopeSpec as mandatory for learned artifacts | Prevents memory pollution and unsafe generalization | Trace summaries becoming unverified beliefs | After first learning pipeline prototype |
| 2026-06-10 | CAK | Cut v0.1 to tool-boundary governance and trace | Proves enforceable value before learning, registry, multi-agent, or provider portability | Scope collapse and architecture-only progress | After one real agent integration |
| 2026-06-10 | CAK | Require a credential-owning tool gateway for governed actions | Policy cannot be enforced if the agent process holds direct tool credentials | Advisory-only capability checks and kernel bypass | During first runtime prototype |
| 2026-06-10 | CAK | Define replay as semantic replay for v0.1 | Live systems, model drift, and provider nondeterminism make byte-identical replay unrealistic | False determinism claims | After first replay harness |
| 2026-06-10 | CAK | Prefer existing predicate and policy languages before inventing one | CEL, Cedar, and Rego may cover v0.1 needs with less risk | Building a hidden general-purpose DSL too early | Before PolicySpec v0.1 freeze |
| 2026-06-10 | CAK | Avoid numeric confidence until calibration exists | False precision weakens EvidenceSpec trust | Magic confidence scores becoming product semantics | Before first promotion verifier |
