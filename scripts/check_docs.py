#!/usr/bin/env python3
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
required = [
    'README.md',
    'docs/00_project_thesis.md',
    'docs/01_pain_map.md',
    'docs/02_full_solution_architecture.md',
    'docs/04_cak_ir_core.md',
    'schemas/cak_ir.schema.json',
    'schemas/task_capsule.schema.json',
    'schemas/effect_spec.schema.json',
    'schemas/skill_spec.schema.json',
    'schemas/policy_spec.schema.json',
    'examples/invoice_agent.cak.yaml',
    'prompts/CODEX_CREATE_PUBLIC_REPO.md',
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print('Missing required files:')
    for p in missing:
        print(' -', p)
    sys.exit(1)

for p in sorted((root / 'schemas').glob('*.json')):
    with p.open('r', encoding='utf-8') as f:
        json.load(f)

print('CAK docs check passed.')
