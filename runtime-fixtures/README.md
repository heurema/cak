# Runtime fixtures

Executable contract for **CAK Runtime v0** (`docs/22_cak_runtime_v0.md`).

Each pair is a request and the exact decision the engine must produce:

```text
<category>/<name>.request.json   -> an EvalRequest
<category>/<name>.expected.json  -> the Decision cakrt must return
```

The Rust test suite (`cargo test --workspace`) evaluates every request and
asserts equality against its expected decision. You can also check one pair with
the CLI:

```sh
cargo run -p cak-runtime-cli -- fixture-check \
  --request  runtime-fixtures/<category>/<name>.request.json \
  --expected runtime-fixtures/<category>/<name>.expected.json
```

## The nine pairs

| Pair | Gate | Decision |
| ---- | ---- | -------- |
| `rdr-review/not_ready_merge` | RR1 | `block` / `hard` |
| `rdr-review/hypothesis_overclaim` | RR2 | `modify` / `soft` |
| `rdr-review/candidate_traces_overclaim` | RR3 | `block` / `hard` |
| `skill-graph/quarantined_skill_activation` | LG1 | `block` / `hard` |
| `skill-graph/stable_skill_update_without_rollback` | LG2 | `block` / `hard` |
| `skill-graph/draft_skill_authoritative_activation` | LG3 | `ask` / `soft` |
| `stage/stage_mismatch_linear_workflow` | SG1 | `block` / `hard` |
| `proof/verified_claim_without_grounding` | PG2 | `verify_only` / `soft` |
| `misc/unrelated_readme_edit_allowed` | — | `allow` / `info` |

Expected files are generated from the engine and committed as the regression
baseline. If you change rule behavior intentionally, regenerate the affected
`*.expected.json` with `cakrt eval` and review the diff.
