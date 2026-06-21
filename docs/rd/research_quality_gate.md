# CAK Research Quality Gate

The quality gate classifies research maturity. It does not decide architecture
by itself.

## Statuses

### Exploratory

Early notes, not decision-grade.

Exploratory material can contain leads, questions, rough hypotheses, and seed
references. It should not be used to justify architecture decisions.

### Research-ready

Enough sources and search plan to start an RDR.

Research-ready means the question is scoped, the source classes are known, and
the run can begin source discovery and evidence extraction.

### Decision-ready

Strong enough for architecture choice.

Decision-ready means the run has enough evidence, counterevidence, adversarial
review, and experiment framing for a human to choose adopt, reject, defer, or
prototype deeper.

### Implementation-ready

Decision + experiment + test plan.

Implementation-ready means a human decision exists and the next change has a
bounded experiment, acceptance criteria, tests, and rollback path.

### Standardization-ready

At least two runtimes/adapters or conformance tests.

Standardization-ready means the protocol candidate is not just one runtime's
internal API.

## Decision-ready requirements

- at least 3 credible sources;
- at least 1 primary paper or official docs for academic/technical claims;
- at least 1 implementation repo or concrete artifact for engineering topics;
- at least 1 counterexample / limitation / negative result;
- `source_ledger.yaml` complete enough to audit claims;
- `pattern_matrix` complete enough to audit borrowed ideas;
- adversarial review completed;
- minimal experiment described;
- kill criteria described;
- human-software default analyzed;
- agent-native alternatives considered.

## Standardization-ready requirements

- at least two independent runtimes/adapters OR conformance tests;
- package/security model specified;
- compatibility story;
- failure and rollback story;
- evidence that the protocol is not just one runtime's internal API.

## Anti-patterns

- "RDR by vibe"
- "single prompt research"
- "citation stuffing"
- "only papers, no implementation"
- "only repos, no theory"
- "no negative evidence"
- "premature protocol"
- "assuming human software abstractions transfer"
- "pattern copying without agent-native adaptation"
- "social signal treated as truth"
- "judge introduces unsupported claims"
- "architecture decided before minimal experiment"

## Gate outcomes

The gate should end with one of:

- pass to the next status;
- remain at current status with missing artifacts listed;
- narrow the research question;
- require more source discovery;
- require adversarial review or debate;
- reject or quarantine the idea through kill criteria.

Gate outcomes should be recorded in `decision_packet.md`.
