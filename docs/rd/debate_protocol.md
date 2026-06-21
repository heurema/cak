# CAK R&D Debate Protocol

Deep research should not rely on one model pass. Use structured disagreement and evidence audit.

## Roles

### Scout

Finds papers, repos, specs, negative results, security analyses, and stronger
analogues.

### Archivist

Builds source ledger, claim matrix, and pattern matrix.

### Builder

Proposes CAK-native design candidates.

### Skeptic

Attacks assumptions and identifies human-software defaults.

### Alienist

Proposes non-obvious / agent-native alternatives that are not direct copies of
human software engineering.

### Security reviewer

Looks for unsafe execution, supply-chain risks, data exfiltration, prompt
injection, approval widening, and self-poisoning.

### Evaluator

Defines metrics, minimal experiments, kill criteria, and comparison baselines.

### Judge

Synthesizes, but cannot introduce unsupported claims.

## Debate modes

### Parallel review

Reviewers independently inspect the same research packet.

Use when source quality, pattern transfer, or architecture pressure needs
independent assessment.

### Actor/critic

One agent defends a hypothesis, another attacks.

Use when a candidate design is plausible but may hide weak assumptions.

### Red-team

Adversary tries to show why the design will fail.

Use for runtime hooks, skill admission, package trust, policy widening, and
anything that may become a security boundary.

### Evidence audit

Reviewer checks whether claims are actually supported by sources.

Use before an RDR enters decision-ready status.

### Pattern audit

Reviewer checks whether a borrowed pattern actually transfers to AI agents.

Use when the run borrows from human software engineering, planning systems,
papers, or external agent frameworks.

## Pattern references

- nitpicker-style multi-review suggests useful patterns: parallel reviewers,
  actor/critic debate, aggregator/meta-reviewer, repo tools, transcripts,
  provider diversity.
- CAK should extract these patterns into its own document process rather than
  depend on a particular tool.

These references are not evidence until inspected and recorded in the source
ledger.

## `debate.md` requirements

`debate.md` must include:

- participants / model providers if known
- prompts used
- positions
- objections
- concessions
- unresolved disagreements
- judge synthesis
- changes made to the RDR after debate

## Judge constraints

The judge can:

- compare positions;
- summarize supported claims;
- identify unresolved disagreements;
- request source-ledger updates;
- request new experiments;
- recommend decision status.

The judge cannot:

- introduce unsupported claims;
- hide counterevidence;
- turn seed references into evidence;
- decide architecture before a minimal experiment;
- override the quality gate.
