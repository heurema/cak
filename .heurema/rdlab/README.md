# CAK R&D Lab

This directory is the CAK project-local R&D Lab OS layer.

Canonical path:

```text
.heurema/rdlab/
```

Use it for project research configuration, topic tracking, source snapshots,
subscription provider routing, research runs, decisions, ideas, experiments,
and promoted memory. Source snapshots check entries in `sources.toml` where
`watch = true`.

CAK research still keeps decision-grade RDR packets under `docs/rd/`. This
project lab tracks portable research workflow state, watched source inputs, and
future project-local runs under the `.heurema/rdlab/` namespace.

Do not create `.rdlab/`. Heurema project tooling should stay under the single
`.heurema/` namespace.

## Typical commands

```bash
python3 /path/to/rd-lab-os/scripts/validate_project.py /path/to/project
python3 /path/to/rd-lab-os/scripts/new_run.py "topic" --project-root /path/to/project
python3 /path/to/rd-lab-os/scripts/snapshot_sources.py /path/to/project
python3 /path/to/rd-lab-os/scripts/provider_router.py doctor --project-root /path/to/project
python3 /path/to/rd-lab-os/scripts/provider_router.py route --project-root /path/to/project --task critic --exclude-provider anthropic
```
