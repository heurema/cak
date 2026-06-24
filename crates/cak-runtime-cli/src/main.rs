//! `cak` — the public CLI over the CAK Runtime v0 core.
//!
//! The CLI does the I/O the core refuses to do (read a file, print JSON) and
//! nothing else. It never evaluates anything itself; it hands the parsed
//! [`EvalRequest`] to the core and reports the [`cak_runtime_core::Decision`].
//!
//! ## Exit-code policy
//!
//! `block` is a domain decision, not a process error. By default `eval` exits
//! `0` for **any** valid decision, including `block`. Exit `1` is reserved for
//! invalid input or a runtime error. With `--enforce-exit-code`, a `block`
//! decision exits `2` so a host can treat it as a gate failure in CI.

use std::path::{Path, PathBuf};
use std::process::ExitCode;

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
