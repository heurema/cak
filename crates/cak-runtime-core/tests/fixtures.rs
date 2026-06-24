//! Fixture-check integration: every request fixture must evaluate to its
//! expected decision fixture, byte-for-byte at the JSON-value level.

use std::path::{Path, PathBuf};

use cak_runtime_core::{evaluate, EvalRequest};
use pretty_assertions::assert_eq;

/// The 9 canonical request/expected fixture pairs.
const FIXTURES: &[&str] = &[
    "rdr-review/not_ready_merge",
    "rdr-review/hypothesis_overclaim",
    "rdr-review/candidate_traces_overclaim",
    "skill-graph/quarantined_skill_activation",
    "skill-graph/stable_skill_update_without_rollback",
    "skill-graph/draft_skill_authoritative_activation",
    "stage/stage_mismatch_linear_workflow",
    "proof/verified_claim_without_grounding",
    "misc/unrelated_readme_edit_allowed",
];

fn fixtures_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("..")
        .join("runtime-fixtures")
}

fn read_json(path: &Path) -> serde_json::Value {
    let raw = std::fs::read_to_string(path)
        .unwrap_or_else(|err| panic!("reading {}: {err}", path.display()));
    serde_json::from_str(&raw).unwrap_or_else(|err| panic!("parsing {}: {err}", path.display()))
}

#[test]
fn all_fixtures_match_expected_decisions() {
    let root = fixtures_root();
    for name in FIXTURES {
        let request_path = root.join(format!("{name}.request.json"));
        let expected_path = root.join(format!("{name}.expected.json"));

        let request: EvalRequest = serde_json::from_value(read_json(&request_path))
            .unwrap_or_else(|err| panic!("deserializing request {name}: {err}"));
        let actual = serde_json::to_value(evaluate(&request)).expect("decision serializes");
        let expected = read_json(&expected_path);

        assert_eq!(actual, expected, "fixture mismatch: {name}");
    }
}

#[test]
fn every_fixture_pair_exists() {
    let root = fixtures_root();
    for name in FIXTURES {
        assert!(
            root.join(format!("{name}.request.json")).exists(),
            "missing request fixture: {name}"
        );
        assert!(
            root.join(format!("{name}.expected.json")).exists(),
            "missing expected fixture: {name}"
        );
    }
}
