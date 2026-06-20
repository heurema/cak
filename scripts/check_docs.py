#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:
    print(f"Missing validation dependency: {exc.name}", file=sys.stderr)
    print("Install PyYAML and jsonschema before running this check.", file=sys.stderr)
    sys.exit(1)


root = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "evidence/README.md",
    "evidence/p0_pain_sources.md",
    "docs/00_project_thesis.md",
    "docs/01_pain_map.md",
    "docs/02_full_solution_architecture.md",
    "docs/04_cak_ir_core.md",
    "docs/10_roadmap.md",
    "docs/13_v0_1_wedge_and_non_goals.md",
    "docs/14_grounding_enforcement_replay.md",
    "docs/15_authoring_economics.md",
    "docs/16_cak_failure_modes.md",
    "docs/20_v0_1_cel_policies.md",
    "docs/21_contract_type_system_skills.md",
    "docs/rd/README.md",
    "docs/rd/00_rd_charter.md",
    "docs/rd/rdr_template.md",
    "docs/rd/01_research_questions.md",
    "docs/rd/02_literature_anchors.md",
    "schemas/cak_ir.schema.json",
    "schemas/task_capsule.schema.json",
    "schemas/effect_spec.schema.json",
    "schemas/skill_spec.schema.json",
    "schemas/policy_spec.schema.json",
    "schemas/contract_spec.schema.json",
    "examples/invoice_agent.cak.yaml",
    "examples/policy_pack.yaml",
    "examples/provider_profile.yaml",
    "examples/task_capsule.yaml",
    "examples/v0_2/contract_specs.yaml",
]


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate(schema, instance, label):
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
    if not errors:
        return

    print(f"Validation failed for {label}:", file=sys.stderr)
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        print(f" - {path}: {error.message}", file=sys.stderr)
    sys.exit(1)


missing = [path for path in required if not (root / path).exists()]
if missing:
    print("Missing required files:", file=sys.stderr)
    for path in missing:
        print(f" - {path}", file=sys.stderr)
    sys.exit(1)

schemas = {}
for path in sorted((root / "schemas").glob("*.json")):
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    schemas[path.name] = schema

invoice = load_yaml(root / "examples/invoice_agent.cak.yaml")
validate(
    schemas["effect_spec.schema.json"],
    invoice["effect"],
    "examples/invoice_agent.cak.yaml#effect",
)
validate(
    schemas["skill_spec.schema.json"],
    invoice["skill"],
    "examples/invoice_agent.cak.yaml#skill",
)
validate(
    schemas["policy_spec.schema.json"],
    invoice["policy"],
    "examples/invoice_agent.cak.yaml#policy",
)

policy_pack = load_yaml(root / "examples/policy_pack.yaml")
for index, policy in enumerate(policy_pack["policies"]):
    validate(
        schemas["policy_spec.schema.json"],
        policy,
        f"examples/policy_pack.yaml#policies[{index}]",
    )

task_capsule = load_yaml(root / "examples/task_capsule.yaml")
validate(schemas["task_capsule.schema.json"], task_capsule, "examples/task_capsule.yaml")

contract_pack = load_yaml(root / "examples/v0_2/contract_specs.yaml")
for index, contract in enumerate(contract_pack["contracts"]):
    validate(
        schemas["contract_spec.schema.json"],
        contract,
        f"examples/v0_2/contract_specs.yaml#contracts[{index}]",
    )

# Parse-only until ProviderProfile gets its own schema.
load_yaml(root / "examples/provider_profile.yaml")

print("CAK docs check passed.")
