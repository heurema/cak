# 14 - Grounding, Enforcement, and Replay

## Why this document exists

Three parts of CAK are make-or-break for the first usable system:

- grounding: how real-world state becomes checkable state;
- enforcement: where CAK actually blocks unsafe actions;
- replay: what kind of repeatability CAK can honestly provide.

These must be designed before learning compilers, artifact registries, or
provider portability.

## Grounding

Grounding is the process that maps external observations into typed state that
policies and effect checks can evaluate.

Example:

```text
customer.exists(email=customer_email)
```

This predicate is not magic. CAK must know:

- which system is authoritative for `customer`;
- which credential or service account can read it;
- how fresh the state must be;
- how stale or partial reads are represented;
- what happens when the environment model disagrees with the live system.

## EnvSpec responsibilities

`EnvSpec` should define:

- authoritative systems and entities;
- state readers and their freshness guarantees;
- action surfaces and side effects;
- hazards and irreversible operations;
- sandbox, staging, and live boundaries;
- data classes and retention constraints;
- drift signals that invalidate prior checks.

v0.1 should not try to model every external system. It should model one narrow
tool boundary well enough to support real policy decisions.

## Enforcement point

CAK enforcement is real only when CAK controls the tool boundary.

The runtime pattern should be:

```text
Agent process
  -> CAK proposal gateway
  -> verifier
  -> tool gateway with credentials
  -> external system
```

The agent must not hold direct credentials for tools that CAK is expected to
govern. If API keys or OAuth tokens remain inside the agent process, CAK is only
advisory and can be bypassed.

## Credential and identity rule

Capabilities must bind to real execution identity:

- service account;
- OAuth subject;
- OIDC claim;
- IAM role;
- local OS user;
- tool-specific token scope.

Approval tokens must be typed, scoped, logged, expiring, and non-replayable.

## Policy and predicate language

v0.1 should not invent a policy language unless reuse fails.

Candidate languages:

| Candidate | Good for | Risk |
|---|---|---|
| CEL | Embedded predicates and simple runtime checks | Not a full authorization system |
| Cedar | Authorization and principal/action/resource policies | More rigid data model |
| Rego | Rich policy-as-code and audits | Operational complexity |

The default v0.1 direction is:

```text
CEL for local predicates.
Cedar or Rego only if authorization complexity requires it.
```

## Replay semantics

CAK should not promise perfect deterministic replay of live agent behavior.

LLM output, provider behavior, UI state, SaaS APIs, clocks, and third-party data
can all drift. Instead, v0.1 should define semantic replay:

```text
recorded proposal
recorded policy decision
recorded tool call
recorded tool result or stub
semantic checkpoints
expected policy outcome
expected external-state diff
```

Replay should answer whether the same policy and effect interpretation still
holds, not whether the model emits byte-identical text.

## Replay modes

| Mode | Purpose |
|---|---|
| Trace replay | Re-run recorded proposals and tool results through current verifiers |
| Stubbed tool replay | Re-run with captured tool responses |
| Snapshot replay | Re-run against a saved environment snapshot |
| Shadow replay | Re-run a task in sandbox or dry-run mode |
| Drift replay | Re-run checks after policy, provider, or environment change |

## Privacy tension

Replay and audit require traces. Privacy and retention rules may require data
deletion.

CAK must separate:

- immutable metadata and decision hashes;
- redacted trace payloads;
- encrypted or separately retained sensitive payloads;
- deletion markers for erased payloads;
- replay fixtures that do not contain raw personal data.

Tombstones alone are not enough when the payload itself must be erased.

## Confidence semantics

CAK should avoid false precision in evidence.

Until there is a calibrated model, examples should prefer:

```text
support_count
counterexample_count
confidence_model: uncalibrated
confidence_label: low | medium | high
```

Numeric confidence can be added later when a documented update rule exists.

## Why not existing tools

CAK should be positioned against composition of existing systems:

| Existing tool class | Covers | CAK gap |
|---|---|---|
| OpenTelemetry | Generic traces | Agent effects, capabilities, learning artifacts |
| LangSmith / Weave / Phoenix | Observability and eval workflows | Enforcement at tool boundary |
| OPA / Cedar | Policy decisions | Agent-specific effects, traces, promotion, unlearning |
| Temporal / Restate | Durable workflows and sagas | Semantic action proposals and policy evidence |
| Vector memory | Recall | Evidence, scope, counterexamples, retraction |

If these tools cover the v0.1 use case with much lower cost, CAK should simplify
or integrate with them instead of duplicating them.

