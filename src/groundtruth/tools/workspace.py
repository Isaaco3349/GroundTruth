"""Sandboxed file and shell tools within the workspace root."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

from groundtruth.config import is_vercel

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


def verify_sample_greet(workspace: Path) -> tuple[int, str]:
    """Run the sample greet assertion without pytest (for lean serverless runtimes)."""
    expected = infer_expected_from_tests(workspace)
    if not expected:
        return 1, "Could not read expected greet() value from tests."

    if is_vercel():
        module_path = workspace / "sampledemo" / "__init__.py"
        if not module_path.is_file():
            return 1, "sampledemo module missing in workspace."
        root = str(workspace)
        if root not in sys.path:
            sys.path.insert(0, root)
        spec = importlib.util.spec_from_file_location("sampledemo", module_path)
        if spec is None or spec.loader is None:
            return 1, "Could not load sampledemo."
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        actual = mod.greet("builder")
        if actual != expected:
            return 1, f"got {actual!r} expected {expected!r}"
        return 0, "sample verification passed"

    script = (
        "import sys\n"
        f"sys.path.insert(0, {str(workspace)!r})\n"
        "from sampledemo import greet\n"
        f"expected = {expected!r}\n"
        "actual = greet('builder')\n"
        "assert actual == expected, f'got {{actual!r}} expected {{expected!r}}'\n"
        "print('sample verification passed')\n"
    )
    code, out, err = run_command(workspace, ["python", "-c", script])
    combined = (out + "\n" + err).strip()
    return code, combined


def run_tests(workspace: Path, *, prefer_pytest: bool = True) -> tuple[int, str]:
    if not prefer_pytest:
        return verify_sample_greet(workspace)
    code, output = run_pytest(workspace)
    if code == 0:
        return code, output
    if "no module named pytest" in output.lower():
        return verify_sample_greet(workspace)
    return code, output


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
