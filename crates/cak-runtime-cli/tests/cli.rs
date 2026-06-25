//! CLI integration: exit-code policy and command behavior for `cak`.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

const BIN: &str = env!("CARGO_BIN_EXE_cak");

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

fn temp_root(name: &str) -> PathBuf {
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    let root = std::env::temp_dir().join(format!(
        "cak-cli-test-{name}-{}-{nonce}",
        std::process::id()
    ));
    fs::create_dir_all(&root).expect("create temp root");
    root
}

#[test]
fn eval_block_exits_zero_by_default() {
    let output = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("rdr-review/not_ready_merge"))
        .output()
        .expect("run cak");
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
        .expect("run cak");
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
        .expect("run cak");
    assert_eq!(status.code(), Some(0));

    // `allow` likewise.
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(request("misc/unrelated_readme_edit_allowed"))
        .arg("--enforce-exit-code")
        .status()
        .expect("run cak");
    assert_eq!(status.code(), Some(0));
}

#[test]
fn eval_missing_file_exits_one() {
    let status = Command::new(BIN)
        .arg("eval")
        .arg("--request")
        .arg(fixtures_root().join("does_not_exist.json"))
        .status()
        .expect("run cak");
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
        .expect("run cak");
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
        .expect("run cak");
    assert_eq!(status.code(), Some(1));
}

#[test]
fn gate_denies_blocking_decision_by_default_with_zero_exit() {
    let output = Command::new(BIN)
        .arg("gate")
        .arg("--proposal")
        .arg(request("rdr-review/pending_trace_status_blocked"))
        .output()
        .expect("run cak gate");
    assert_eq!(
        output.status.code(),
        Some(0),
        "gate must exit 0 by default for a valid deny outcome"
    );

    let outcome: serde_json::Value =
        serde_json::from_slice(&output.stdout).expect("stdout is JSON");
    assert_eq!(outcome["outcome"], "deny");
    assert_eq!(outcome["decision"]["decision"], "block");
    assert_eq!(outcome["decision"]["selected_evaluator"], "rdr_review");
}

#[test]
fn gate_denies_blocking_decision_with_exit_two_when_enforced() {
    let status = Command::new(BIN)
        .arg("gate")
        .arg("--proposal")
        .arg(request("rdr-review/pending_trace_status_blocked"))
        .arg("--enforce-exit-code")
        .status()
        .expect("run cak gate");
    assert_eq!(
        status.code(),
        Some(2),
        "deny must exit 2 under --enforce-exit-code"
    );
}

#[test]
fn gate_allows_non_rdr_mark_ready() {
    let output = Command::new(BIN)
        .arg("gate")
        .arg("--proposal")
        .arg(request("rdr-review/non_rdr_mark_ready_allowed"))
        .output()
        .expect("run cak gate");
    assert_eq!(output.status.code(), Some(0));

    let outcome: serde_json::Value =
        serde_json::from_slice(&output.stdout).expect("stdout is JSON");
    assert_eq!(outcome["outcome"], "proceed");
    assert_eq!(outcome["decision"]["decision"], "allow");
}

#[test]
fn skill_init_creates_package_skeleton() {
    let root = temp_root("skill-init");

    let status = Command::new(BIN)
        .arg("skill")
        .arg("init")
        .arg("demo-review")
        .arg("--host")
        .arg("codex")
        .arg("--output")
        .arg(&root)
        .status()
        .expect("run cak skill init");
    assert_eq!(status.code(), Some(0));

    let package = root.join("demo-review");
    let skill = fs::read_to_string(package.join("SKILL.md")).expect("read SKILL.md");
    let descriptor = fs::read_to_string(package.join("cak.yaml")).expect("read cak.yaml");

    assert!(skill.contains("name: demo-review"));
    assert!(skill.contains("description:"));
    assert!(descriptor.contains("id: local.demo-review"));
    assert!(descriptor.contains("version: 0.1.0"));
    assert!(descriptor.contains("kind: package"));
    assert!(package.join("fixtures/allow.request.json").exists());
    assert!(package.join("fixtures/block.request.json").exists());
}

#[test]
fn skill_check_accepts_generated_package() {
    let root = temp_root("skill-check");
    let package = root.join("demo-review");

    let init_status = Command::new(BIN)
        .arg("skill")
        .arg("init")
        .arg("demo-review")
        .arg("--output")
        .arg(&root)
        .status()
        .expect("run cak skill init");
    assert_eq!(init_status.code(), Some(0));

    let check_status = Command::new(BIN)
        .arg("skill")
        .arg("check")
        .arg(&package)
        .status()
        .expect("run cak skill check");
    assert_eq!(check_status.code(), Some(0));
}

#[test]
fn skill_check_rejects_missing_skill_frontmatter() {
    let root = temp_root("skill-check-invalid");
    let package = root.join("broken-skill");
    fs::create_dir_all(&package).expect("create package");
    fs::write(package.join("SKILL.md"), "# Broken\n").expect("write SKILL.md");
    fs::write(
        package.join("cak.yaml"),
        "id: local.broken-skill\nversion: 0.1.0\nkind: package\n",
    )
    .expect("write cak.yaml");

    let output = Command::new(BIN)
        .arg("skill")
        .arg("check")
        .arg(&package)
        .output()
        .expect("run cak skill check");

    assert_eq!(output.status.code(), Some(1));
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("SKILL.md frontmatter"), "{stderr}");
}

#[test]
fn skill_install_copies_package_and_records_metadata() {
    let root = temp_root("skill-install");
    let target = root.join("codex-skills");
    let package = root.join("demo-review");

    let init_status = Command::new(BIN)
        .arg("skill")
        .arg("init")
        .arg("demo-review")
        .arg("--output")
        .arg(&root)
        .status()
        .expect("run cak skill init");
    assert_eq!(init_status.code(), Some(0));

    let install_status = Command::new(BIN)
        .arg("skill")
        .arg("install")
        .arg(&package)
        .arg("--host")
        .arg("codex")
        .arg("--target")
        .arg(&target)
        .status()
        .expect("run cak skill install");
    assert_eq!(install_status.code(), Some(0));

    let installed = target.join("demo-review");
    assert!(installed.join("SKILL.md").exists());
    assert!(installed.join("cak.yaml").exists());

    let metadata: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(installed.join(".cak-install.json")).unwrap())
            .expect("metadata is JSON");
    assert_eq!(metadata["installed_by"], "cak");
    assert_eq!(metadata["host"], "codex");
    assert_eq!(metadata["skill_id"], "local.demo-review");
    assert_eq!(metadata["version"], "0.1.0");
    assert_eq!(metadata["source_path"], package.to_string_lossy().as_ref());
}

#[test]
fn skill_install_rejects_source_target_overlap() {
    let root = temp_root("skill-install-overlap");
    let package = root.join("demo-review");

    let init_status = Command::new(BIN)
        .arg("skill")
        .arg("init")
        .arg("demo-review")
        .arg("--output")
        .arg(&root)
        .status()
        .expect("run cak skill init");
    assert_eq!(init_status.code(), Some(0));

    let output = Command::new(BIN)
        .arg("skill")
        .arg("install")
        .arg(&package)
        .arg("--target")
        .arg(&root)
        .output()
        .expect("run cak skill install");

    assert_eq!(output.status.code(), Some(1));
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(
        stderr.contains("would copy the skill package into itself"),
        "{stderr}"
    );
}
