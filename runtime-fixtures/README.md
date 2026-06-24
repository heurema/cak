# Runtime fixtures

Executable contract for **CAK Runtime v0** (`docs/22_cak_runtime_v0.md`).

Each pair is a request and the exact decision the engine must produce:

```text
<category>/<name>.request.json   -> an EvalRequest
<category>/<name>.expected.json  -> the Decision cak must return
```

The Rust test suite (`cargo test --workspace`) evaluates every request and
asserts equality against its expected decision. You can also check one pair with
the CLI:

```sh
cargo run -p cak-runtime-cli -- fixture-check \
  --request  runtime-fixtures/<category>/<name>.request.json \
  --expected runtime-fixtures/<category>/<name>.expected.json
```

## The fifteen pairs

| Pair | Gate | Decision |
| ---- | ---- | -------- |
| `rdr-review/not_ready_merge` | RR1 | `block` / `hard` |
| `rdr-review/hypothesis_overclaim` | RR2 | `modify` / `soft` |
| `rdr-review/candidate_traces_overclaim` | RR3 | `block` / `hard` |
| `rdr-review/missing_trace_status_blocked` | RR3 | `block` / `hard` |
| `rdr-review/pending_trace_status_blocked` | RR3 | `block` / `hard` |
| `rdr-review/non_rdr_mark_ready_allowed` | — | `allow` / `info` |
| `skill-graph/quarantined_skill_activation` | LG1 | `block` / `hard` |
| `skill-graph/stable_skill_update_without_rollback` | LG2 | `block` / `hard` |
| `skill-graph/draft_skill_authoritative_activation` | LG3 | `ask` / `soft` |
| `skill-graph/quarantined_skill_authority_claim` | LG4 | `block` / `hard` |
| `stage/stage_mismatch_linear_workflow` | SG1 | `block` / `hard` |
| `stage/mark_ready_preconditions_missing` | SG2 | `ask` / `soft` |
| `proof/verified_claim_without_grounding` | PG2 | `verify_only` / `soft` |
| `proof/failed_verifier_text_overclaim` | PG4 | `block` / `hard` |
| `misc/unrelated_readme_edit_allowed` | — | `allow` / `info` |

Expected files are generated from the engine and committed as the regression
baseline. If you change rule behavior intentionally, regenerate the affected
`*.expected.json` with `cak eval` and review the diff.
