# Predicate-language comparison (exp-005, lab / q-003)

Decides whether CAK adopts CEL, Cedar, or Rego for `PolicySpec` predicates
instead of the interim restricted surface. Pre-registered in
`lab/experiments/exp-005-predicate-language.md`.

## Corpus

10 policies drawn from the real v0.1 configs (invoice example, exp-004
boundaries) plus two cases the interim surface cannot express:

| Id | Rule | Interim surface |
|---|---|---|
| P1 | amount > 10000 -> require_approval (2 actions) | yes |
| P2 | amount <= 0 -> block | yes |
| P3 | refund amount > 200 -> require_approval | yes |
| P4 | environment == "production" -> require_approval | yes |
| P5 | unconditional warn on key rotation | yes (after empty-when fix) |
| P6 | refund without reason -> block | no (no negation/absence) |
| P7 | close without resolution note -> block | no (same) |
| P8 | unconditional block on delete | yes (after empty-when fix) |
| P9 | refund amount > order_total -> block | **no (cross-field)** |
| P10 | environment not in allowed list -> block | **no (membership)** |

15 scenarios in `scenarios.json` exercise every policy both ways; expected
outcome = strictest-wins enforcement, mirroring the cak verifier.

## Results — day 1, 2026-06-12

Install cost (measured): OPA 45 s (brew), cel-python 10 s (pip/venv),
Cedar CLI 71 s (cargo).

| Language | Correctness | p50 / p99 per decision | Mode |
|---|---|---|---|
| CEL (celpy) | 15/15 | 0.20 ms / 0.37 ms | in-process Python |
| Rego (opa eval) | 15/15 | 12.1 ms / 14.4 ms | CLI subprocess |
| Cedar (cedar authorize) | 15/15 | 13.1 ms / 15.8 ms | CLI subprocess ×3 tiers |

All three cover the full corpus, including everything the interim surface
cannot. All fit the 50 ms p99 budget even in their slowest embedding mode.

Notes per language:

- **CEL**: maps 1:1 onto the existing config shape (policy = expression +
  scope + enforcement); in-process evaluation needs no subprocess; absence
  check is `!('field' in args)`.
- **Rego**: full coverage, natural set/negation syntax; per-decision CLI
  cost ~12 ms would need the Go SDK or a server mode for in-process use.
- **Cedar**: full coverage but no native enforcement tiers — encoded as
  three policy stores queried in order (block, require_approval, warn);
  that is a real contortion. Carries the strongest formal-verification
  story (cedar-symcc, radar finding 2026-06-11).

## Formal-tooling axis — 2026-06-12

What is actually runnable today, checked on this machine:

| Language | Static checking | Symbolic/formal verification |
|---|---|---|
| Cedar | `cedar validate` against a schema — **runs, all three stores pass** (`cedar/schema.cedarschema`) | `cedar-policy-symcc` 0.5.2 exists but is a **library** (Cedar→SMT, needs a Rust harness + cvc5/z3); no turnkey CLI |
| CEL | type-checked compile against a declared environment (celpy/cel-go) | none mainstream; the guarantee is structural — non-Turing-complete, terminating, cost-bounded in cel-go |
| Rego | `opa check`, `opa test`, coverage | none mainstream |

Reading: Cedar's formal story is real but engineering-gated; CEL's guarantee
is weaker but free; Rego sits between with the best test tooling.

## Authoring-ergonomics axis — 2026-06-12

Cold-draft protocol from exp-004: prose brief of the 10 corpus rules +
per-language format reference (`authoring/inputs/`), empty temp dir, output
scored by the same 15 scenarios.

| Drafter | CEL | Rego | Cedar (3 stores) |
|---|---|---|---|
| claude sonnet | 15/15, 17 s | 15/15, 23 s | 15/15, 30 s |
| codex (OpenAI) | 15/15, 22 s | 15/15, 19 s | 15/15, 24 s |

**6/6 perfect, zero correction cycles.** The authoring axis does not
discriminate: all three languages are drafting-friendly for this corpus.
Drafts preserved under `authoring/drafts/`.

## Summary across all axes

| Axis | CEL | Rego | Cedar |
|---|---|---|---|
| Corpus coverage | 10/10 | 10/10 | 10/10 (tier encoding contortion) |
| Embedding | **in-process, 10 s install** | subprocess or Go SDK, 45 s | subprocess ×3, 71 s |
| Latency p99 | **0.37 ms** | 14.4 ms | 15.8 ms |
| Termination guarantee | by design | by design | by design |
| Formal tooling | none (structural only) | tests/coverage | **validate runs; symcc (lib-only)** |
| Cold-draft authoring | 15/15 ×2 vendors | 15/15 ×2 vendors | 15/15 ×2 vendors |

## Proposed verdict (for q-003 / cak docs/11 — owner ratifies)

Adopt **CEL** for `PolicySpec.when` expressions in v0.2:

- only in-process option for the Python runtime — no subprocess in the
  enforcement hot path, 50–80× under the latency budget;
- maps 1:1 onto the existing config shape: CAK keeps the PolicySpec
  envelope (action scope, enforcement tiers, strictest-wins) and adopts a
  predicate *language*, not a policy *framework*;
- cheapest embedding, terminating by design, vendor-neutral spec.

Positioning of the others: **Rego** — mechanical translation target when an
org already runs OPA (proven by this corpus); **Cedar** — keep as a future
*verification export* target: compile PolicySpec tiers to Cedar stores (this
experiment did it by hand) and run schema validation / symcc when formal
guarantees become a product requirement.

## Reproduce

```sh
brew install opa && cargo install cedar-policy-cli
python3 -m venv /tmp/exp005-venv && /tmp/exp005-venv/bin/pip install cel-python
/tmp/exp005-venv/bin/python experiments/predicate-language/run_comparison.py
```
