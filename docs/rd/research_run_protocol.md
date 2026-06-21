# CAK Research Run Protocol

An RDR is not a prompt output. An RDR is the compressed result of a research run.

A research run is:

```text
research question
-> research plan
-> source discovery
-> pattern extraction
-> source ledger
-> claim matrix
-> hypothesis matrix
-> adversarial review
-> debate / multi-review
-> evidence quality gate
-> RDR draft
-> human decision
```

A model may propose claims, but only the source ledger can support claims.

## Required artifacts

Each research run should produce these artifacts before its RDR is considered
decision-grade.

### `research_plan.md`

Defines the research question, scope, source strategy, exclusion rules,
expected objections, and minimal experiments. It is the run contract.

### `source_ledger.yaml`

Records every inspected source, its class, reliability, extracted claims,
counterclaims, quoted support, limitations, and extracted patterns. This is the
only artifact that can support claims in an RDR.

### `pattern_matrix.md`

Extracts reusable patterns from sources and explains what transfers, what does
not transfer, and how the pattern might become agent-native in CAK.

### `claim_matrix.md`

Maps explicit claims to supporting sources, challenging sources, confidence,
limitations, and whether the claim is used in the RDR.

### `hypothesis_matrix.md`

Compares candidate hypotheses, the evidence for and against them, required
experiments, expected failures, and kill criteria.

### `adversarial_review.md`

Attacks the run's assumptions, source quality, claim support, human-software
defaults, architecture pressure, security risks, and missing counterevidence.

### `debate.md`

Captures structured disagreement between reviewers, including positions,
objections, concessions, unresolved disagreements, judge synthesis, and changes
made after debate.

### `decision_packet.md`

Summarizes what a human decision-maker needs: research question, supported
claims, unresolved unknowns, minimal experiment, kill criteria, decision options,
and recommended next step.

## Research plan

`research_plan.md` must include:

- research question
- scope
- non-goals
- seed sources
- search queries
- source classes to inspect
- exclusion criteria
- expected counterarguments
- minimal experiment candidates

The plan should say what would be enough to stop, defer, reject, or narrow the
run before more research time is spent.

## Source discovery

Source discovery must inspect multiple source classes when relevant:

- academic papers
- implementation repos
- official docs/specs
- benchmarks/evals
- negative results
- security analyses
- community/practitioner signals
- related protocols
- older AI/planning/cognitive-architecture ideas when relevant

Important: Pattern references can inspire discovery methods, but they are not
accepted evidence until inspected and recorded in `source_ledger.yaml`.

Discovery should prefer primary sources, working artifacts, reproducible
benchmarks, and negative evidence over summaries. Secondary sources can help
find leads, but they do not replace inspection.

## Pattern extraction

For every useful pattern, record:

```yaml
pattern:
source:
what to copy:
what not to copy:
agent-native adaptation:
risk:
evidence status:
```

Examples of pattern categories:

- horizon scanning
- multi-source discovery
- source scoring
- grounded synthesis
- parallel reviewers
- actor/critic debate
- aggregator / meta-reviewer
- provider diversity
- transcript / trajectory logs
- evidence audit
- verifier-gated admission
- counterexample-driven revision
- maturity-aware update gating
- rollback validation
- precondition/postcondition memory
- model-checker filtering
- skill supply-chain analysis

Pattern extraction is not adoption. A pattern becomes useful only after the run
explains what transfers to AI agents, what fails to transfer, and what evidence
would distinguish the hypotheses.

## Evidence extraction

Claims must be rewritten into explicit form:

```yaml
claim:
source:
supporting passage:
why it matters:
limitations:
confidence:
```

Rules:

- Do not cite a source unless it was inspected.
- Do not convert social signal into truth.
- Do not treat a paper claim as engineering proof without implementation or
  evaluation evidence.
- Do not treat a repo as theory without asking what it assumes, omits, and
  fails to measure.
- Record counterevidence and limitations next to the claim they weaken.

## Adversarial review

Every decision-grade run needs at least one adversarial review. The review
should ask:

- Which claims lack source-ledger support?
- Which sources are weak, stale, uninspected, or secondary?
- Which human-software defaults are being smuggled in?
- Which agent-native alternatives were not considered?
- Which negative results or security analyses are missing?
- Which proposed patterns fail to transfer?
- Which architecture decisions are being made before experiment?

## Debate / multi-review

Use the debate protocol when a run affects architecture, security, protocol
surface, runtime semantics, or standardization claims. Debate outputs should
update one of:

- `source_ledger.yaml`
- `pattern_matrix.md`
- `claim_matrix.md`
- `hypothesis_matrix.md`
- `adversarial_review.md`
- `decision_packet.md`

The judge may synthesize positions, but cannot introduce unsupported claims.

## Evidence quality gate

The quality gate decides whether the run is exploratory, research-ready,
decision-ready, implementation-ready, or standardization-ready. Passing the gate
does not decide architecture. It only says the research packet is strong enough
for the next decision.

## RDR draft

An RDR is downstream of the run. It should compress:

- the research question;
- the relevant claims and counterclaims;
- the human-software default;
- why that default may fail for agents;
- candidate hypotheses;
- non-obvious alternatives;
- minimal experiment;
- evaluation criteria;
- kill criteria;
- recommended decision or deferral.

## Decision readiness

A research run is decision-ready only when:

- source ledger is non-empty;
- pattern matrix is non-empty for design questions;
- counterevidence is represented;
- at least one adversarial review exists;
- open unknowns are listed;
- minimal experiment is specified;
- kill criteria are specified.

Decision-ready does not mean implementation-ready. Implementation still requires
a human decision, experiment scope, test plan, and rollback path.
