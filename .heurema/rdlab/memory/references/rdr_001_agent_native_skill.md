# RDR-001 Reference Catalog

Source of truth: `docs/rd/runs/rdr_001_agent_native_skill/source_ledger.yaml`.

This catalog mirrors the inspected anchors used by the RDR-001 research packet
so the project-local R&D Lab OS layer can route future research without
re-reading the full ledger first. Claims still need to cite the source ledger,
not this summary.

## Core Papers

| Source ledger ID | Reference | URL | Role |
|---|---|---|---|
| `src_hasp_arxiv` | Harnessing LLM Agents with Skill Programs | https://arxiv.org/abs/2605.17734 | Program Function / active-skill anchor |
| `src_awm_arxiv` | Agent Workflow Memory | https://arxiv.org/abs/2409.07429 | Workflow-memory anchor |
| `src_voyager_arxiv` | Voyager: An Open-Ended Embodied Agent with Large Language Models | https://arxiv.org/abs/2305.16291 | Executable-code skill baseline |
| `src_vaso_arxiv` | VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents | https://arxiv.org/abs/2606.05395 | Contract and verifier-facing skill anchor |
| `src_psn_arxiv` | Evolving Programmatic Skill Networks | https://arxiv.org/abs/2601.03509 | Executable symbolic skill network and lifecycle anchor |
| `src_hmt_arxiv` | Enhancing Web Agents with a Hierarchical Memory Tree | https://arxiv.org/abs/2603.07024 | Stage-aware procedural-memory anchor |
| `src_skillwiki_arxiv` | SkillWiki: A Living Knowledge Infrastructure for Agent Skills | https://arxiv.org/abs/2606.16523 | Provenance and lifecycle infrastructure anchor |
| `src_skillrevise_arxiv` | SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision | https://arxiv.org/abs/2606.01139 | Diagnosis and repair anchor |
| `src_skilljuror_arxiv` | SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior | https://arxiv.org/abs/2606.11543 | Package organization and runtime-capture anchor |
| `src_skillreducer_arxiv` | SkillReducer: Optimizing LLM Agent Skills for Token Efficiency | https://arxiv.org/abs/2603.29919 | Routing and progressive-disclosure quality anchor |

## Security Papers

| Source ledger ID | Reference | URL | Role |
|---|---|---|---|
| `src_skillinject_arxiv` | Skill-Inject: Measuring Agent Vulnerability to Skill File Attacks | https://arxiv.org/abs/2602.20156 | Skill-file prompt-injection risk |
| `src_skillject_arxiv` | SkillJect: Effectively Automating Skill-Based Prompt Injection for Skill-Enabled Agents | https://arxiv.org/abs/2602.14211 | Cross-file poisoned-skill attack mechanics |
| `src_malskillbench_arxiv` | MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills | https://arxiv.org/abs/2606.07131 | Runtime-verified malicious skill benchmark |
| `src_repo_context_security_arxiv` | Context Matters: Repository-Aware Security Analysis of the Agent Skill Ecosystem | https://arxiv.org/abs/2603.16572 | Repository-context security analysis |

## Specs And Repositories

| Source ledger ID | Reference | URL | Role |
|---|---|---|---|
| `src_agent_skills_spec` | Agent Skills specification | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md | Package/distribution baseline |
| `src_voyager_repo` | Voyager implementation repository | https://github.com/MineDojo/Voyager | Executable skill-library implementation artifact |
| `src_skillwiki_repo` | SkillWiki implementation repository | https://github.com/Huangdingcheng/SkillWiki | Provenance/lifecycle implementation artifact |
| `src_skilljuror_repo` | SkillJuror implementation repository | https://github.com/zhiyuchen-ai/skill-juror | Package-variant and runtime-capture artifact |
| `src_skillinject_repo` | Skill-Inject benchmark repository | https://github.com/aisa-group/skill-inject | Sandboxed hostile-skill benchmark artifact |
| `src_promptinject_agent_skills_repo` | Prompt injection agent-skills research repository | https://github.com/aisa-group/promptinject-agent-skills | Poisoned-skill fixture artifact |

## Use Rules

- Use this file as an index only.
- Use `source_ledger.yaml` as the evidence boundary for claims.
- Keep uninspected leads out of project decisions until they are promoted into
  the source ledger with `inspected: true`.
- Treat GitHub repositories as implementation leads unless the ledger records
  stronger validation than README-level inspection.
