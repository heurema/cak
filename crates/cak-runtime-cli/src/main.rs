//! `cak` — the public CLI over the CAK Runtime v0 core.
//!
//! The CLI does the I/O the core refuses to do: read files, print JSON, and
//! manage host-facing skill packages. It never evaluates runtime decisions
//! itself; it hands parsed [`EvalRequest`] values to the core and reports the
//! [`cak_runtime_core::Decision`].
//!
//! ## Exit-code policy
//!
//! `block` is a domain decision, not a process error. By default `eval` exits
//! `0` for **any** valid decision, including `block`. Exit `1` is reserved for
//! invalid input or a runtime error. With `--enforce-exit-code`, a `block`
//! decision exits `2` so a host can treat it as a gate failure in CI.

use std::path::{Path, PathBuf};
use std::process::ExitCode;
use std::time::{SystemTime, UNIX_EPOCH};

use anyhow::Context;
use cak_host_adapter::{HostOutcomeKind, HostProposal};
use cak_runtime_core::{DecisionKind, EvalRequest};
use clap::{Parser, Subcommand};

/// CAK Runtime v0 decision engine CLI.
#[derive(Debug, Parser)]
#[command(name = "cak", version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Evaluate an EvalRequest and print the Decision as pretty JSON.
    Eval {
        /// Path to the EvalRequest JSON file.
        #[arg(long)]
        request: PathBuf,
        /// Exit 2 when `decision == block` (default: exit 0 for any valid
        /// decision).
        #[arg(long)]
        enforce_exit_code: bool,
    },
    /// Evaluate an EvalRequest and compare the Decision to an expected fixture.
    FixtureCheck {
        /// Path to the EvalRequest JSON file.
        #[arg(long)]
        request: PathBuf,
        /// Path to the expected Decision JSON fixture.
        #[arg(long)]
        expected: PathBuf,
    },
    /// Evaluate a host proposal and print a host-facing outcome as pretty JSON.
    Gate {
        /// Path to the host proposal JSON file.
        #[arg(long)]
        proposal: PathBuf,
        /// Exit 2 when `outcome == deny` (default: exit 0 for any valid
        /// outcome).
        #[arg(long)]
        enforce_exit_code: bool,
    },
    /// Create, validate, and install CAK-compatible skill packages.
    Skill {
        #[command(subcommand)]
        command: SkillCommand,
    },
}

#[derive(Debug, Subcommand)]
enum SkillCommand {
    /// Create a local skill package skeleton.
    Init {
        /// Skill folder/name, for example `demo-review`.
        name: String,
        /// Host template to generate.
        #[arg(long, default_value = "codex")]
        host: String,
        /// Directory where the new skill folder is created.
        #[arg(long, default_value = ".")]
        output: PathBuf,
    },
    /// Validate a CAK-compatible skill package.
    Check {
        /// Path to the skill package folder.
        path: PathBuf,
    },
    /// Install a checked skill package into a host skill directory.
    Install {
        /// Path to the skill package folder.
        path: PathBuf,
        /// Host target to install for. v0 supports `codex`.
        #[arg(long, default_value = "codex")]
        host: String,
        /// Host skill directory to install into.
        #[arg(long)]
        target: PathBuf,
    },
}

#[derive(Debug)]
struct SkillPackage {
    id: String,
    version: String,
    kind: String,
    required_fixtures: Vec<PathBuf>,
}

fn main() -> ExitCode {
    match run(Cli::parse()) {
        Ok(code) => code,
        Err(err) => {
            // Any I/O or parse failure is a process error: exit 1.
            eprintln!("error: {err:#}");
            ExitCode::from(1)
        }
    }
}

fn run(cli: Cli) -> anyhow::Result<ExitCode> {
    match cli.command {
        Command::Eval {
            request,
            enforce_exit_code,
        } => cmd_eval(&request, enforce_exit_code),
        Command::FixtureCheck { request, expected } => cmd_fixture_check(&request, &expected),
        Command::Gate {
            proposal,
            enforce_exit_code,
        } => cmd_gate(&proposal, enforce_exit_code),
        Command::Skill { command } => match command {
            SkillCommand::Init { name, host, output } => cmd_skill_init(&name, &host, &output),
            SkillCommand::Check { path } => cmd_skill_check(&path),
            SkillCommand::Install { path, host, target } => {
                cmd_skill_install(&path, &host, &target)
            }
        },
    }
}

fn read_request(path: &Path) -> anyhow::Result<EvalRequest> {
    let raw = std::fs::read_to_string(path)
        .with_context(|| format!("reading request file {}", path.display()))?;
    cak_runtime_core::parse_request(&raw)
        .with_context(|| format!("parsing request file {}", path.display()))
}

fn cmd_eval(path: &Path, enforce_exit_code: bool) -> anyhow::Result<ExitCode> {
    let request = read_request(path)?;
    let decision = cak_runtime_core::evaluate(&request);
    println!("{}", serde_json::to_string_pretty(&decision)?);

    if enforce_exit_code && decision.decision == DecisionKind::Block {
        Ok(ExitCode::from(2))
    } else {
        Ok(ExitCode::SUCCESS)
    }
}

fn cmd_fixture_check(request_path: &Path, expected_path: &Path) -> anyhow::Result<ExitCode> {
    let request = read_request(request_path)?;
    let decision = cak_runtime_core::evaluate(&request);
    let actual = serde_json::to_value(&decision).context("serializing decision")?;

    let expected_raw = std::fs::read_to_string(expected_path)
        .with_context(|| format!("reading expected fixture {}", expected_path.display()))?;
    let expected: serde_json::Value = serde_json::from_str(&expected_raw)
        .with_context(|| format!("parsing expected fixture {}", expected_path.display()))?;

    if actual == expected {
        println!(
            "ok: {} matches {}",
            request_path.display(),
            expected_path.display()
        );
        return Ok(ExitCode::SUCCESS);
    }

    eprintln!("mismatch: {}", request_path.display());
    report_diff(&expected, &actual);
    Ok(ExitCode::from(1))
}

fn read_proposal(path: &Path) -> anyhow::Result<HostProposal> {
    read_request(path).with_context(|| format!("parsing proposal file {}", path.display()))
}

fn cmd_gate(path: &Path, enforce_exit_code: bool) -> anyhow::Result<ExitCode> {
    let proposal = read_proposal(path)?;
    let outcome = cak_host_adapter::evaluate_proposal(&proposal);
    println!("{}", serde_json::to_string_pretty(&outcome)?);

    if enforce_exit_code && outcome.outcome == HostOutcomeKind::Deny {
        Ok(ExitCode::from(2))
    } else {
        Ok(ExitCode::SUCCESS)
    }
}

fn cmd_skill_init(name: &str, host: &str, output: &Path) -> anyhow::Result<ExitCode> {
    validate_skill_name(name)?;
    validate_host(host)?;

    let package_dir = output.join(name);
    if package_dir.exists() {
        anyhow::bail!("skill package already exists: {}", package_dir.display());
    }

    std::fs::create_dir_all(package_dir.join("fixtures"))
        .with_context(|| format!("creating skill package {}", package_dir.display()))?;
    std::fs::write(package_dir.join("SKILL.md"), skill_md_template(name, host))
        .with_context(|| format!("writing {}", package_dir.join("SKILL.md").display()))?;
    std::fs::write(package_dir.join("cak.yaml"), cak_yaml_template(name))
        .with_context(|| format!("writing {}", package_dir.join("cak.yaml").display()))?;
    std::fs::write(
        package_dir.join("fixtures/allow.request.json"),
        fixture_template(name, "allow"),
    )
    .with_context(|| {
        format!(
            "writing {}",
            package_dir.join("fixtures/allow.request.json").display()
        )
    })?;
    std::fs::write(
        package_dir.join("fixtures/block.request.json"),
        fixture_template(name, "block"),
    )
    .with_context(|| {
        format!(
            "writing {}",
            package_dir.join("fixtures/block.request.json").display()
        )
    })?;

    println!("created skill package: {}", package_dir.display());
    Ok(ExitCode::SUCCESS)
}

fn cmd_skill_check(path: &Path) -> anyhow::Result<ExitCode> {
    let package = validate_skill_package(path)?;
    println!(
        "ok: {} ({}, {})",
        path.display(),
        package.id,
        package.version
    );
    Ok(ExitCode::SUCCESS)
}

fn cmd_skill_install(path: &Path, host: &str, target: &Path) -> anyhow::Result<ExitCode> {
    validate_host(host)?;
    let package = validate_skill_package(path)?;
    let folder_name = path
        .file_name()
        .and_then(|name| name.to_str())
        .context("skill package path must end with a folder name")?;
    validate_skill_name(folder_name)?;

    std::fs::create_dir_all(target)
        .with_context(|| format!("creating target directory {}", target.display()))?;
    let source_dir = path
        .canonicalize()
        .with_context(|| format!("resolving skill package {}", path.display()))?;
    let target_dir = target
        .canonicalize()
        .with_context(|| format!("resolving target directory {}", target.display()))?;
    let install_dir = target_dir.join(folder_name);
    if install_dir == source_dir || install_dir.starts_with(&source_dir) {
        anyhow::bail!(
            "install target would copy the skill package into itself: {}",
            install_dir.display()
        );
    }
    if install_dir.exists() {
        anyhow::bail!(
            "install directory already exists: {}; remove it before install",
            install_dir.display()
        );
    }

    std::fs::create_dir_all(&install_dir)
        .with_context(|| format!("creating install directory {}", install_dir.display()))?;
    copy_dir_contents(&source_dir, &install_dir)?;

    let installed_at = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .context("system clock is before Unix epoch")?
        .as_secs();
    let metadata = serde_json::json!({
        "installed_by": "cak",
        "host": host,
        "skill_id": package.id,
        "version": package.version,
        "kind": package.kind,
        "source_path": source_dir.to_string_lossy(),
        "install_path": install_dir.to_string_lossy(),
        "installed_at_unix": installed_at,
    });
    std::fs::write(
        install_dir.join(".cak-install.json"),
        serde_json::to_string_pretty(&metadata)?,
    )
    .with_context(|| {
        format!(
            "writing install metadata {}",
            install_dir.join(".cak-install.json").display()
        )
    })?;

    println!("installed skill package: {}", install_dir.display());
    Ok(ExitCode::SUCCESS)
}

/// Print a human-readable diff between expected and actual decisions.
///
/// Lists the top-level keys that differ, then dumps both pretty bodies so the
/// mismatch is easy to eyeball.
fn report_diff(expected: &serde_json::Value, actual: &serde_json::Value) {
    if let (Some(expected_map), Some(actual_map)) = (expected.as_object(), actual.as_object()) {
        let mut keys: Vec<&String> = expected_map.keys().chain(actual_map.keys()).collect();
        keys.sort_unstable();
        keys.dedup();
        for key in keys {
            let lhs = expected_map.get(key);
            let rhs = actual_map.get(key);
            if lhs != rhs {
                eprintln!("  field `{key}` differs:");
                eprintln!("    expected: {}", render(lhs));
                eprintln!("    actual:   {}", render(rhs));
            }
        }
    }

    eprintln!(
        "--- expected\n{}",
        serde_json::to_string_pretty(expected).unwrap_or_default()
    );
    eprintln!(
        "--- actual\n{}",
        serde_json::to_string_pretty(actual).unwrap_or_default()
    );
}

fn render(value: Option<&serde_json::Value>) -> String {
    match value {
        Some(value) => value.to_string(),
        None => "<absent>".to_string(),
    }
}

fn validate_host(host: &str) -> anyhow::Result<()> {
    if host == "codex" {
        Ok(())
    } else {
        anyhow::bail!("unsupported host `{host}`; v0 supports `codex`")
    }
}

fn validate_skill_name(name: &str) -> anyhow::Result<()> {
    let valid = !name.is_empty()
        && name.len() <= 63
        && name
            .bytes()
            .all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'-')
        && !name.starts_with('-')
        && !name.ends_with('-');
    if valid {
        Ok(())
    } else {
        anyhow::bail!("invalid skill name `{name}`; use lowercase letters, digits, and hyphens")
    }
}

fn validate_skill_package(path: &Path) -> anyhow::Result<SkillPackage> {
    if !path.is_dir() {
        anyhow::bail!("skill package is not a directory: {}", path.display());
    }

    let skill_path = path.join("SKILL.md");
    let descriptor_path = path.join("cak.yaml");
    let skill = std::fs::read_to_string(&skill_path)
        .with_context(|| format!("reading {}", skill_path.display()))?;
    validate_skill_frontmatter(&skill)
        .with_context(|| format!("invalid SKILL.md frontmatter in {}", skill_path.display()))?;

    let descriptor = std::fs::read_to_string(&descriptor_path)
        .with_context(|| format!("reading {}", descriptor_path.display()))?;
    let package = parse_skill_descriptor(&descriptor)
        .with_context(|| format!("invalid cak.yaml in {}", descriptor_path.display()))?;

    validate_fixture_requests(path, &package.required_fixtures)?;

    Ok(package)
}

fn validate_skill_frontmatter(raw: &str) -> anyhow::Result<()> {
    let mut lines = raw.lines();
    if lines.next() != Some("---") {
        anyhow::bail!("SKILL.md frontmatter must start with `---`");
    }

    let mut has_name = false;
    let mut has_description = false;
    for line in lines {
        let trimmed = line.trim();
        if trimmed == "---" {
            if has_name && has_description {
                return Ok(());
            }
            anyhow::bail!("SKILL.md frontmatter must include name and description");
        }
        has_name |= trimmed.starts_with("name:") && !trimmed["name:".len()..].trim().is_empty();
        has_description |= trimmed.starts_with("description:")
            && !trimmed["description:".len()..].trim().is_empty();
    }

    anyhow::bail!("SKILL.md frontmatter must end with `---`")
}

fn parse_skill_descriptor(raw: &str) -> anyhow::Result<SkillPackage> {
    let id = top_level_scalar_value(raw, "id").context("missing id")?;
    let version = top_level_scalar_value(raw, "version").context("missing version")?;
    let kind = top_level_scalar_value(raw, "kind").context("missing kind")?;
    let required_fixtures = list_values(raw, "required_fixtures")
        .context("missing required_fixtures")?
        .into_iter()
        .map(|value| validate_relative_fixture_path(&value))
        .collect::<anyhow::Result<Vec<_>>>()?;

    if !id.starts_with("local.") && !id.starts_with("cak.") {
        anyhow::bail!("id must start with `local.` or `cak.`");
    }
    if version.is_empty() {
        anyhow::bail!("version must not be empty");
    }
    if !matches!(
        kind.as_str(),
        "package" | "workflow" | "verifier" | "intervention" | "hybrid"
    ) {
        anyhow::bail!("unsupported kind `{kind}`");
    }

    for required in [
        "host_package:",
        "runtime:",
        "admission:",
        "trust:",
        "entrypoint: SKILL.md",
        "maturity: draft",
    ] {
        if !raw.lines().any(|line| line.trim() == required) {
            anyhow::bail!("missing `{required}`");
        }
    }

    if required_fixtures.is_empty() {
        anyhow::bail!("required_fixtures must not be empty");
    }

    Ok(SkillPackage {
        id,
        version,
        kind,
        required_fixtures,
    })
}

fn top_level_scalar_value(raw: &str, key: &str) -> Option<String> {
    let prefix = format!("{key}:");
    raw.lines().find_map(|line| {
        let trimmed = line.trim_end();
        if trimmed.len() != trimmed.trim_start().len() {
            return None;
        }
        trimmed
            .strip_prefix(&prefix)
            .map(str::trim)
            .filter(|value| !value.is_empty())
            .map(|value| value.trim_matches('"').trim_matches('\'').to_string())
    })
}

fn list_values(raw: &str, key: &str) -> Option<Vec<String>> {
    let header = format!("{key}:");
    let lines: Vec<_> = raw.lines().collect();
    for (index, line) in lines.iter().enumerate() {
        if line.trim() != header {
            continue;
        }

        let header_indent = indentation(line);
        let mut values = Vec::new();
        for item in lines.iter().skip(index + 1) {
            if item.trim().is_empty() {
                continue;
            }
            if indentation(item) <= header_indent {
                break;
            }
            let trimmed = item.trim();
            if let Some(value) = trimmed.strip_prefix("- ") {
                let value = value.trim().trim_matches('"').trim_matches('\'');
                if !value.is_empty() {
                    values.push(value.to_string());
                }
            }
        }

        return Some(values);
    }

    None
}

fn indentation(line: &str) -> usize {
    line.len() - line.trim_start().len()
}

fn validate_relative_fixture_path(value: &str) -> anyhow::Result<PathBuf> {
    let path = PathBuf::from(value);
    if path.is_absolute()
        || path.components().any(|component| {
            matches!(
                component,
                std::path::Component::ParentDir
                    | std::path::Component::RootDir
                    | std::path::Component::Prefix(_)
            )
        })
    {
        anyhow::bail!(
            "required fixture path must be relative and stay inside the package: {value}"
        );
    }
    Ok(path)
}

fn validate_fixture_requests(path: &Path, required_fixtures: &[PathBuf]) -> anyhow::Result<()> {
    for relative_path in required_fixtures {
        let fixture_path = path.join(relative_path);
        if !fixture_path.is_file() {
            anyhow::bail!("missing required fixture: {}", relative_path.display());
        }
        parse_fixture_request(&fixture_path)?;
    }

    let fixtures_dir = path.join("fixtures");
    if !fixtures_dir.exists() {
        return Ok(());
    }

    for entry in std::fs::read_dir(&fixtures_dir)
        .with_context(|| format!("reading fixtures directory {}", fixtures_dir.display()))?
    {
        let entry = entry?;
        let fixture_path = entry.path();
        let is_request_json = fixture_path
            .file_name()
            .and_then(|name| name.to_str())
            .is_some_and(|name| name.ends_with(".request.json"));
        if !is_request_json {
            continue;
        }

        parse_fixture_request(&fixture_path)?;
    }

    Ok(())
}

fn parse_fixture_request(fixture_path: &Path) -> anyhow::Result<()> {
    let raw = std::fs::read_to_string(fixture_path)
        .with_context(|| format!("reading fixture {}", fixture_path.display()))?;
    cak_runtime_core::parse_request(&raw)
        .with_context(|| format!("parsing fixture {}", fixture_path.display()))?;
    Ok(())
}

fn copy_dir_contents(source: &Path, target: &Path) -> anyhow::Result<()> {
    for entry in std::fs::read_dir(source)
        .with_context(|| format!("reading skill package {}", source.display()))?
    {
        let entry = entry?;
        let source_path = entry.path();
        let target_path = target.join(entry.file_name());
        let file_type = entry.file_type()?;

        if file_type.is_dir() {
            std::fs::create_dir_all(&target_path)
                .with_context(|| format!("creating directory {}", target_path.display()))?;
            copy_dir_contents(&source_path, &target_path)?;
        } else if file_type.is_file() {
            std::fs::copy(&source_path, &target_path).with_context(|| {
                format!(
                    "copying {} to {}",
                    source_path.display(),
                    target_path.display()
                )
            })?;
        }
    }

    Ok(())
}

fn skill_md_template(name: &str, host: &str) -> String {
    format!(
        r#"---
name: {name}
description: Use when a {host} agent should load the {name} CAK-compatible skill package.
---

# {name}

This is a CAK-compatible host skill package.

Run `cak skill check` before installing it into a host.
"#
    )
}

fn cak_yaml_template(name: &str) -> String {
    format!(
        r#"id: local.{name}
version: 0.1.0
kind: package

host_package:
  format: agent_skill
  entrypoint: SKILL.md

runtime:
  kind: package
  boundary: eval_request_decision

admission:
  maturity: draft
  required_fixtures:
    - fixtures/allow.request.json
    - fixtures/block.request.json

trust:
  network_required: false
  side_effect_class: repo_docs_only
"#
    )
}

fn fixture_template(name: &str, fixture_kind: &str) -> String {
    let (request_id, task_kind, proposed_action, maturity) = match fixture_kind {
        "block" => (
            format!("{name}-blocked-authority-smoke"),
            "custom_skill_admission_smoke",
            serde_json::json!({
                "kind": "claim_authority",
                "skill_id": format!("local.{name}"),
                "authority": "authoritative"
            }),
            "quarantined",
        ),
        _ => (
            format!("{name}-allow-smoke"),
            "custom_skill_admission_smoke",
            serde_json::json!({
                "kind": "read_file",
                "target": "README.md"
            }),
            "draft",
        ),
    };

    serde_json::to_string_pretty(&serde_json::json!({
        "schema_version": cak_runtime_core::SCHEMA_VERSION,
        "request_id": request_id,
        "host": { "name": "cak-skill-check", "mode": "test" },
        "task": {
            "kind": task_kind,
            "goal": "Validate the custom skill package fixture shape."
        },
        "proposed_action": proposed_action,
        "skill": { "id": format!("local.{name}"), "version": "0.1.0" },
        "skill_graph": {
            "nodes": [
                {
                    "id": format!("local.{name}"),
                    "kind": "package",
                    "version": "0.1.0",
                    "lifecycle": {
                        "maturity": maturity,
                        "health": "unknown"
                    },
                    "provenance_refs": ["local.template"]
                }
            ],
            "edges": []
        }
    }))
    .expect("template JSON serializes")
}
