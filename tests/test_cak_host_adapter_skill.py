import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cak-host-adapter" / "scripts" / "cak_gate.py"


def test_skill_shim_delegates_to_cakrt_gate(tmp_path: Path) -> None:
    proposal = tmp_path / "proposal.json"
    proposal.write_text('{"schema_version":"0.1.0"}', encoding="utf-8")
    argv_path = tmp_path / "argv.json"

    fake_cakrt = tmp_path / "fake-cakrt"
    fake_cakrt.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, pathlib, sys",
                (
                    f"pathlib.Path({str(argv_path)!r}).write_text("
                    "json.dumps(sys.argv), encoding='utf-8')"
                ),
                "print(json.dumps({'schema_version':'0.1.0','outcome':'proceed'}))",
            ]
        ),
        encoding="utf-8",
    )
    os.chmod(fake_cakrt, 0o755)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--proposal",
            str(proposal),
            "--cakrt",
            str(fake_cakrt),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout)["outcome"] == "proceed"
    assert json.loads(argv_path.read_text(encoding="utf-8")) == [
        str(fake_cakrt),
        "gate",
        "--proposal",
        str(proposal),
    ]
