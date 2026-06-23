# CAK R&D

CAK R&D exists to discover agent-native software abstractions: forms of skills,
procedural memory, contracts, verifiers, traces, and governance that fit AI
agent failure modes instead of copying human software defaults by habit.

R&D precedes architecture for major design decisions. Implementation should
follow only after a Research Decision Record (RDR), a small experiment, or an
explicit implementation spike identifies what should be built and what should
not be built.

Current status: CAK has executable spikes such as the experimental
ContractSpec checker MVP, but those spikes are research artifacts until they
are validated against concrete questions, alternatives, and kill criteria.

Start here:

- [R&D Charter](00_rd_charter.md)
- [Research Run Protocol](research_run_protocol.md)
- [Source Ledger template](source_ledger_template.yaml)
- [Debate Protocol](debate_protocol.md)
- [Research Quality Gate](research_quality_gate.md)
- [Pattern References](pattern_references.md)
- [Skill Architecture Deep Research Synthesis](03_skill_architecture_synthesis.md)
- [Research Runs](runs/README.md)
- [Research Decision Record template](rdr_template.md)
- [Research Question Map](01_research_questions.md)
- [Literature Anchors](02_literature_anchors.md)

RDRs are downstream of research runs. A useful RDR compresses source discovery,
evidence tracking, pattern extraction, adversarial review, debate, quality
gates, unknowns, minimal experiment candidates, and kill criteria.

Pattern references are idea sources, not dependencies. They can guide source
discovery and pattern extraction, but they do not support claims until inspected
and recorded in a source ledger.

Research runs should search for stronger analogues beyond the seed list. The
seed references are starting points, not a boundary around the research space.

The skill architecture synthesis captures the current working hypothesis that
agent-native skills may be compiled bridges between evidence/provenance IR and
runtime-control IR. It is a synthesis note, not a decision-grade RDR.
