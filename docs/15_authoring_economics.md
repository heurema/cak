# 15 - Authoring Economics

## Why this document exists

CAK asks for structured artifacts: effects, environment specs, scopes, policies,
traces, replay checkpoints, and evidence.

That is expensive if humans write everything by hand. Similar model-first
systems failed when annotation cost exceeded operational value.

CAK v0.1 must prove that authoring cost is low enough for real teams.

## Core assumption

CAK only works if agents draft most artifacts and humans review the parts that
carry risk.

```text
agent drafts
human reviews
verifier checks
gateway enforces
trace records
```

The human should not be expected to hand-author full `EffectSpec`, `EnvSpec`,
or `ScopeSpec` documents for every workflow.

## Authoring loop

The intended loop is:

```text
1. Agent proposes a tool call.
2. CAK records the proposal, context, tool result, and policy decision.
3. CAK drafts or updates EffectSpec/PolicySpec candidates from repeated traces.
4. Human reviews a small diff, not a blank spec.
5. Verifier checks syntax, policy coverage, and regression fixtures.
6. Approved artifacts become reusable.
```

This keeps CAK closer to code review than ontology authoring.

## Human responsibilities

Humans should review:

- risky effect classification;
- irreversible or external actions;
- scope expansion;
- policy weakening;
- approval tokens;
- cross-tenant artifact reuse;
- promotion from candidate to active.

Humans should not repeatedly write boilerplate predicates or copy tool schemas
when those can be derived from traces and tool contracts.

## Agent responsibilities

Agents can draft:

- action proposals;
- observed state snapshots;
- effect candidates;
- policy coverage gaps;
- replay fixtures;
- evidence summaries;
- drift patches;
- documentation diffs.

Agent-authored artifacts remain candidates until reviewed and verified.

## Cold start

Evidence-backed learning has a cold-start problem:

- few traces mean weak evidence;
- tight scopes split evidence across tenants, roles, and environments;
- privacy rules limit cross-tenant sharing.

v0.1 should not depend on accumulated learning value. It should deliver value at
Level 1 through tool-boundary checks and traces.

## Domain packs

The first scalable artifact reuse may come from domain packs, not from a global
behavior registry.

Examples:

- GitHub write actions;
- Slack external sends;
- Stripe refunds and charges;
- invoice creation and voiding;
- deployment and rollback actions.

Domain packs can contain reviewed `ActionSpec`, `EffectSpec`, and baseline
policies for common APIs. Teams still bind them to local credentials, scopes,
and approval rules.

## Why this is not Semantic Web redux

CAK should avoid the old failure mode:

```text
human writes complete ontology before value appears
```

The CAK path should be:

```text
tool boundary value first
trace data next
agent-drafted artifacts after repeated use
human promotion only for risk-bearing changes
```

If CAK requires broad manual annotation before value appears, v0.1 should be
considered failed.

## Product vs standard

CAK should start as a product implementation, not as a standards effort.

The schemas define the product's artifact contracts. They should not be treated
as an industry standard until there are independent implementations, real users,
and external contributors with reason to adopt the format.

Near-term priority:

```text
working gateway + useful traces + low-friction adoption
```

not neutral standards governance.

