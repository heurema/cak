#!/usr/bin/env python3
"""Thin Python launcher for `cak gate`.

The policy decision stays in Rust. This script exists so Agent-Skills-style
hosts that expect a Python script can invoke the canonical CAK CLI.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the CAK Rust host adapter gate.",
        allow_abbrev=False,
    )
    parser.add_argument("--proposal", required=True, type=Path, help="Path to proposal JSON.")
    parser.add_argument("--cak", default="cak", help="Path to the cak binary.")
    parser.add_argument(
        "--enforce-exit-code",
        action="store_true",
        help="Exit 2 when the Rust adapter returns outcome=deny.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = [args.cak, "gate", "--proposal", str(args.proposal)]
    if args.enforce_exit_code:
        command.append("--enforce-exit-code")

    result = subprocess.run(command, check=False, capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
