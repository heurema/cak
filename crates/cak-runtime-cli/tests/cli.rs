//! CLI integration: exit-code policy and command behavior for `cakrt`.

use std::path::{Path, PathBuf};
use std::process::Command;

const BIN: &str = env!("CARGO_BIN_EXE_cakrt");

fn fixtures_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("..")
        .join("runtime-fixtures")
}

fn request(name: &str) -> PathBuf {
    fixtures_root().join(format!("{name}.request.json"))
}

fn expected(name: &str) -> PathBuf {
    fixtures_root().join(format!("{name}.expected.json"))
}

#[test]
fn eval_block_exits_zero_by_default() {
    let output = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("rdr-review/not_ready_merge"))
        .output()
        .expect("run cakrt");
    assert_eq!(
        output.status.code(),
        Some(0),
        "block must exit 0 by default"
    );

    let decision: serde_json::Value =
        serde_json::from_slice(&output.stdout).expect("stdout is JSON");
    assert_eq!(decision["decision"], "block");
}

#[test]
fn eval_block_exits_two_with_enforce_flag() {
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("rdr-review/not_ready_merge"))
        .arg("--enforce-exit-code")
        .status()
        .expect("run cakrt");
    assert_eq!(
        status.code(),
        Some(2),
        "block must exit 2 under --enforce-exit-code"
    );
}

#[test]
fn eval_non_block_exits_zero_even_with_enforce_flag() {
    // `ask` is not a block: enforce mode must still exit 0.
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("skill-graph/draft_skill_authoritative_activation"))
        .arg("--enforce-exit-code")
        .status()
        .expect("run cakrt");
    assert_eq!(status.code(), Some(0));

    // `allow` likewise.
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("misc/unrelated_readme_edit_allowed"))
        .arg("--enforce-exit-code")
        .status()
        .expect("run cakrt");
    assert_eq!(status.code(), Some(0));
}

#[test]
fn eval_missing_file_exits_one() {
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(fixtures_root().join("does_not_exist.json"))
        .status()
        .expect("run cakrt");
    assert_eq!(status.code(), Some(1), "missing input must exit 1");
}

#[test]
fn fixture_check_passes_on_match() {
    let status = Command::new(BIN)
        .arg("fixture-check")
        .arg("--request")
        .arg(request("proof/verified_claim_without_grounding"))
        .arg("--expected")
        .arg(expected("proof/verified_claim_without_grounding"))
        .status()
        .expect("run cakrt");
    assert_eq!(status.code(), Some(0));
}

#[test]
fn fixture_check_fails_on_mismatch() {
    // Pair a request with the wrong expected fixture.
    let status = Command::new(BIN)
        .arg("fixture-check")
        .arg("--request")
        .arg(request("proof/verified_claim_without_grounding"))
        .arg("--expected")
        .arg(expected("misc/unrelated_readme_edit_allowed"))
        .status()
        .expect("run cakrt");
    assert_eq!(status.code(), Some(1));
}
