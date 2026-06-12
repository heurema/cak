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

## Remaining before verdict (deadline 2026-07-02)

- Authoring-ergonomics axis: re-run the exp-004 cold-draft protocol with
  policies written in each language.
- Formal-tooling axis: try cedar-symcc on the Cedar tier stores; survey
  CEL/Rego equivalents.

## Reproduce

```sh
brew install opa && cargo install cedar-policy-cli
python3 -m venv /tmp/exp005-venv && /tmp/exp005-venv/bin/pip install cel-python
/tmp/exp005-venv/bin/python experiments/predicate-language/run_comparison.py
```
