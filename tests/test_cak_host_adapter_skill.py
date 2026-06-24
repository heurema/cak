import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cak-host-adapter" / "scripts" / "cak_gate.py"


def write_fake_cak(path: Path, argv_path: Path) -> None:
    path.write_text(
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
    os.chmod(path, 0o755)


def test_skill_shim_delegates_to_cak_gate_from_path(tmp_path: Path) -> None:
    proposal = tmp_path / "proposal.json"
    proposal.write_text('{"schema_version":"0.1.0"}', encoding="utf-8")
    argv_path = tmp_path / "argv.json"

    fake_cak = tmp_path / "cak"
    write_fake_cak(fake_cak, argv_path)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--proposal",
            str(proposal),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}"},
    )

    assert result.returncode == 0
    assert json.loads(result.stdout)["outcome"] == "proceed"
    argv = json.loads(argv_path.read_text(encoding="utf-8"))
    assert Path(argv[0]).name == "cak"
    assert argv[1:] == [
        "gate",
        "--proposal",
        str(proposal),
    ]


def test_skill_shim_rejects_legacy_cakrt_option(tmp_path: Path) -> None:
    proposal = tmp_path / "proposal.json"
    proposal.write_text('{"schema_version":"0.1.0"}', encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--proposal",
            str(proposal),
            "--cakrt",
            str(tmp_path / "cakrt"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "unrecognized arguments: --cakrt" in result.stderr
