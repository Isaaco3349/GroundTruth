"""Sandboxed file and shell tools within the workspace root."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ALLOWED_COMMANDS = frozenset({"python", "pytest", "py"})


def _resolve(workspace: Path, relative: str) -> Path:
    target = (workspace / relative).resolve()
    root = workspace.resolve()
    if not str(target).startswith(str(root)):
        raise PermissionError("Path escapes workspace")
    return target


def read_text_file(workspace: Path, relative: str) -> str:
    path = _resolve(workspace, relative)
    return path.read_text(encoding="utf-8")


def write_text_file(workspace: Path, relative: str, content: str) -> None:
    path = _resolve(workspace, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_command(workspace: Path, argv: list[str], timeout: int = 120) -> tuple[int, str, str]:
    if not argv:
        raise ValueError("Empty command")
    exe = Path(argv[0]).name.lower()
    if exe not in ALLOWED_COMMANDS:
        raise PermissionError(f"Command not allowed: {argv[0]}")

    completed = subprocess.run(
        argv,
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def run_pytest(workspace: Path) -> tuple[int, str]:
    code, out, err = run_command(workspace, ["python", "-m", "pytest", "-q"])
    combined = (out + "\n" + err).strip()
    return code, combined


def reset_sample_bug(workspace: Path) -> bool:
    bug = workspace / "sampledemo" / "__init__.demo_bug.py"
    target = workspace / "sampledemo" / "__init__.py"
    if not bug.is_file() or not target.parent.is_dir():
        return False
    target.write_text(bug.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def infer_expected_from_tests(workspace: Path) -> str | None:
    tests_dir = workspace / "tests"
    if not tests_dir.is_dir():
        return None
    for path in tests_dir.glob("test_*.py"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r'assert\s+greet\([^)]+\)\s*==\s*["\']([^"\']+)["\']', text)
        if match:
            return match.group(1)
    return None
