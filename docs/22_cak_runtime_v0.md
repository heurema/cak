# CAK Runtime v0

Status: v0 executable runtime boundary. First decision engine for CAK skills.

CAK Runtime v0 is a host-neutral **decision engine**. Its entire contract is:

```text
EvalRequest (JSON)  ->  Decision (JSON)
```

Given an in-memory `EvalRequest`, the engine returns a `Decision`. That is all
it does. It is implemented as a small Rust workspace inside this repository:

```text
Cargo.toml                       workspace root (resolver 2, edition 2021)
crates/cak-runtime-core/         the engine: data models + evaluators (no I/O)
crates/cak-runtime-cli/          cakrt: a thin CLI over the core
runtime-fixtures/                request/expected JSON pairs (the contract, executable)
skills/cak-rdr-review/           Agent-Skills-compatible pilot host package
```

## What it is

- A pure, deterministic function from a request to a decision.
- A set of four small **evaluators** (gates) composed by priority.
- A CLI, `cakrt`, that reads a request file and prints a decision.

The design follows the RDR-001 working hypothesis that an agent-native skill is
a *state/action-conditioned intervention* with an activation predicate, a
runtime-loop position, an intervention behavior, and an audit signal — not a
package, a script, or prose. See
`docs/rd/runs/rdr_001_agent_native_skill/programmatic_runtime_skill_scope.md`
and `docs/rd/03_skill_architecture_synthesis.md`.

## What it is not (non-goals)

Runtime v0 is deliberately small. It is **not**:

- an agent framework — it does not own the agent loop;
- a markdown parser — it never reads SKILL.md or any document;
- a GitHub client — it never reads PRs, issues, or repo state;
- a script executor — it never runs skill scripts;
- an MCP server — MCP is a later transport, not part of v0;
- a full harness — admission, replay, shadow mode, and quarantine workflows are
  out of scope;
- a generic SkillPack or rule DSL — rules are Rust code, the contract is fixtures;
- a change to the existing Python runtime — that behavior is untouched.

Two hard invariants back these non-goals:

1. **The core crate never shells out, accesses the network, or reads repo
   state.** It only evaluates an in-memory `EvalRequest`. This is enforced by
   construction: evaluators receive `&EvalRequest` and nothing else.
2. **Runtime facts come from the request JSON, not from filesystem inspection.**
   If a fact is not in the request, it does not exist for the evaluator. The
   host is responsible for gathering facts and encoding them.

## The boundary: EvalRequest -> Decision

`EvalRequest` carries everything the engine may reason about: the host context,
the task, free-form `state`/`artifacts`/`metadata`, the `proposed_action`, the
`skill` reference, and four optional context blocks — `skill_graph`, `stage`,
`proof`, and `provenance`. The contract is expressed as Rust `serde` structs and
JSON fixtures, not as a JSON Schema file. The structs are the schema; the
fixtures are the executable, regression-tested examples.

`Decision` carries the verdict: a `decision` kind, a `severity`, a human
`reason`, the `selected_evaluator`, structured `violations`, an optional
`repair` suggestion, and a `trace` event for audit logs.

```text
decision kinds:  allow | block | modify | inject_context | ask | verify_only
severities:      info | soft | hard
```

A `Decision` is a **domain verdict**, not a process result. In particular,
`decision == block` is a successful, valid evaluation — see the exit-code policy
below.

## Why four evaluators

Each evaluator encodes one independent failure mode drawn from the RDR-001
synthesis. They are separate so each can be reasoned about, tested, and evolved
on its own, and so the composite priority is explicit rather than tangled.

| Evaluator        | Origin            | Guards against |
| ---------------- | ----------------- | -------------- |
| `lifecycle_gate` | PSN / SkillWiki   | activating quarantined/deprecated skills; quarantined/deprecated skills claiming authoritative control; updating stable/protected skills without a rollback checkpoint; immature skills claiming authoritative control |
| `stage_gate`     | HMT / AWM         | completing stage-bound actions while the workflow stage is in mismatch or its preconditions are missing |
| `proof_gate`     | VASO              | claiming verification without a passing verifier; accepting claims with unknown/suspect grounding; prose overclaiming "verified"/"supported" with open obligations or a failed verifier |
| `rdr_review`     | RDR-001 domain    | recommending merge before an RDR packet is decision-ready; overclaiming C10; accepting a trace corpus without a positive `sufficient`/`pass` status |

### Composition

The composite runs the evaluators in a fixed order and resolves one decision:

```text
order:              lifecycle_gate -> stage_gate -> proof_gate -> rdr_review
decision priority:  block > ask > modify > inject_context > verify_only > allow
severity priority:  hard > soft > info
tie-break:          earlier evaluator wins (lifecycle > stage > proof > rdr)
short-circuit:      only on a block/hard decision
```

The winning decision is stamped with its `selected_evaluator`. When no gate
matches, the composite returns a neutral `allow`.

## Exit-code policy

`cakrt eval` distinguishes a **domain decision** from a **process error**:

- exit `0` for any valid decision by default — including `block`;
- exit `1` only for invalid input or a runtime error (missing file, bad JSON, a
  request that does not match the `EvalRequest` shape);
- exit `2` for `decision == block` **only** when `--enforce-exit-code` is passed.

This keeps `block` a first-class domain outcome that a host can inspect without a
non-zero process status, while still allowing CI to treat a block as a gate
failure when it opts in with `--enforce-exit-code`.

## Using the CLI

```sh
# Evaluate a request and print the decision (exit 0 even for block):
cakrt eval --request runtime-fixtures/rdr-review/not_ready_merge.request.json

# Same, but a block decision exits 2 (CI gate mode):
cakrt eval --request <request.json> --enforce-exit-code

# Check a request against its expected decision fixture:
cakrt fixture-check \
  --request  runtime-fixtures/rdr-review/not_ready_merge.request.json \
  --expected runtime-fixtures/rdr-review/not_ready_merge.expected.json
```

A host skill calls the runtime exactly the same way: it assembles an
`EvalRequest` JSON document from whatever facts it has gathered, runs
`cakrt eval --request <path>`, and honors the returned decision. The runtime
decision is authoritative over prose. See `skills/cak-rdr-review/SKILL.md` for
the pilot host package.

## Running the fixtures

There are nine canonical request/expected pairs in `runtime-fixtures/`, one or
more per evaluator plus an allow control. They are the executable contract.

```sh
# Build and run the whole Rust test suite (includes a fixture-check over all 9):
cargo test --workspace

# Or check a single fixture pair with the CLI:
cargo run -p cak-runtime-cli -- fixture-check \
  --request  runtime-fixtures/stage/stage_mismatch_linear_workflow.request.json \
  --expected runtime-fixtures/stage/stage_mismatch_linear_workflow.expected.json
```

Quality gates for the workspace:

```sh
cargo fmt --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

## Why a workspace, not a separate repo yet

The runtime lives inside `heurema/cak` for now because:

- it is co-evolving with the RDR-001 research run and its domain rules
  (`rdr_review`) are CAK-specific;
- keeping it in-repo lets the same CI validate the Rust runtime, the Python
  runtime, and the docs together;
- v0 is small enough that a separate repo would add release and versioning
  overhead before the boundary has stabilized.

### Future extraction path

When the boundary stabilizes, the natural split is:

1. keep `cak-runtime-core` host-neutral and extract it to its own crate/repo,
   published independently;
2. keep `rdr_review` (the CAK-specific gate) in this repo as a downstream
   evaluator that depends on the extracted core;
3. add transports incrementally — CLI first (this PR), then an MCP server as a
   thin adapter over the same `EvalRequest -> Decision` core;
4. grow the Evidence/Runtime IR only as RDRs promote concepts from hypothesis to
   decision. The core stays a pure decision function throughout.

## Initial PR template

```text
Title: feat(runtime): add Rust CAK runtime v0

Summary
- Adds a host-neutral Rust decision engine: EvalRequest -> Decision.
- Two crates: cak-runtime-core (pure, no I/O) and cak-runtime-cli (cakrt).
- Four evaluators (lifecycle, stage, proof, rdr-review) composed by priority.
- Nine request/expected fixtures as the executable contract.
- Agent-Skills-compatible pilot package skills/cak-rdr-review.

Boundary and non-goals
- Not an agent framework, harness, MCP server, markdown parser, GitHub client,
  script executor, or generic rule DSL. Existing Python runtime unchanged.
- Core never shells out, hits the network, or reads repo state. Facts come from
  the request JSON only.

Exit-code decision
- `block` is a valid domain decision: `cakrt eval` exits 0 for any valid
  decision by default. It only exits non-zero for `block` when
  `--enforce-exit-code` is used (then exit 2). Exit 1 is reserved for invalid
  input or runtime error.

Verification
- cargo fmt --check
- cargo clippy --workspace --all-targets -- -D warnings
- cargo test --workspace  (all 9 fixtures pass)
- python3 scripts/check_docs.py and python3 -m pytest still pass.
```
