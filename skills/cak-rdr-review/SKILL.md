---
name: cak-rdr-review
description: Review CAK R&D PRs and research packets for unsupported claims, overclaimed readiness, lifecycle violations, stage mismatches, and missing proof grounding.
---

# CAK RDR Review

This skill gates CAK research-and-development pull requests and research packets
through the **CAK Runtime v0** decision engine (`cak`). It is the pilot host
package for that runtime.

## When to use

Use this skill when an agent is about to:

- recommend merging or marking-ready an RDR research packet;
- claim that a hypothesis-level synthesis (e.g. C10) is a supported decision;
- accept a trace-corpus plan as sufficient experiment evidence;
- activate, update, or claim authority over a skill with lifecycle state;
- complete a stage-bound workflow action;
- assert that something is "verified" or "supported".

If none of these apply, the runtime returns `allow` and the agent proceeds.

## How it works

The runtime is host-neutral: it evaluates an in-memory `EvalRequest` and returns
a `Decision`. It does **not** read GitHub, parse markdown, inspect the repo, or
run scripts. The host agent is responsible for gathering the relevant facts and
encoding them into an `EvalRequest` JSON document.

The contract is:

```text
EvalRequest (JSON)  ->  cak eval  ->  Decision (JSON)
```

The host agent should:

1. Build an `EvalRequest` JSON file describing the proposed action and the
   relevant `state`, `skill_graph`, `stage`, and `proof` facts.
2. Run the runtime:

   ```sh
   cak eval --request <path-to-request.json>
   ```

3. Read the `Decision` from stdout and honor it.

By default `cak eval` exits `0` for **any** valid decision, including `block`
— `block` is a domain verdict, not a process failure. Pass `--enforce-exit-code`
to make a `block` decision exit `2` (useful as a CI gate).

## The runtime decision is authoritative

When the runtime returns `block`, `ask`, `modify`, or `verify_only`, that
decision is authoritative over any prose recommendation in the PR, the SKILL.md,
or the agent's own narration. Prose advises; the Rust decision governs. Do not
override a `block` with a natural-language justification.

## Examples

### 1. Not decision-ready merge

The packet is still exploratory, but the agent wants to recommend merge.

Request (`state.decision_packet_status` is not `decision_ready`):

```json
{
  "schema_version": "0.1.0",
  "host": { "name": "cak-rdr-review", "mode": "ci" },
  "task": { "kind": "review_rdr_pr" },
  "state": { "decision_packet_status": "exploratory" },
  "proposed_action": { "kind": "recommend_merge", "target": "pr/10" },
  "skill": { "id": "cak.rdr-review" }
}
```

Decision: `block` / `hard` — *"Research packet is not decision-ready."*

### 2. C10 hypothesis overclaim

The agent claims the compiled-bridge synthesis (C10) is a supported decision,
but C10 is hypothesis-level.

Request (`state.c10_status` is `hypothesis_level`, action text mentions C10):

```json
{
  "schema_version": "0.1.0",
  "host": { "name": "cak-rdr-review", "mode": "ci" },
  "task": { "kind": "review_rdr_claim" },
  "state": { "c10_status": "hypothesis_level" },
  "proposed_action": {
    "kind": "claim_supported",
    "text": "C10 is a supported architecture decision."
  },
  "skill": { "id": "cak.rdr-review" }
}
```

Decision: `modify` / `soft` — reframe C10 as hypothesis-level synthesis, not a
supported architecture decision.

### 3. Candidate trace corpus overclaim

The agent wants to accept a trace-corpus plan that is only candidate-level.

Request (`state.trace_plan_status` is `candidate_only`):

```json
{
  "schema_version": "0.1.0",
  "host": { "name": "cak-rdr-review", "mode": "ci" },
  "task": { "kind": "review_trace_corpus" },
  "state": { "trace_plan_status": "candidate_only" },
  "proposed_action": { "kind": "accept_trace_corpus" },
  "skill": { "id": "cak.rdr-review" }
}
```

Decision: `block` / `hard` unless `state.trace_plan_status` is `sufficient`
or `pass` — *"Trace corpus plan is not sufficient."*

## Fixtures

Worked request/expected pairs live in `runtime-fixtures/`. Verify any of them:

```sh
cak fixture-check \
  --request runtime-fixtures/rdr-review/not_ready_merge.request.json \
  --expected runtime-fixtures/rdr-review/not_ready_merge.expected.json
```

See `docs/22_cak_runtime_v0.md` for the full runtime design, non-goals, and the
`EvalRequest -> Decision` contract.
