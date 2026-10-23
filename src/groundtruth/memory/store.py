"""Local memory for stack notes and recent runs."""

from __future__ import annotations

import json

from groundtruth.config import runtime_data_dir


def _memory_path():
    path = runtime_data_dir() / "memory" / "profile.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_profile() -> dict:
    path = _memory_path()
    if not path.is_file():
        return {"notes": [], "recent_run_ids": []}
    return json.loads(path.read_text(encoding="utf-8"))


def remember_run(run_id: str, task: str) -> None:
    try:
        path = _memory_path()
        profile = load_profile()
        recent = [run_id] + [r for r in profile.get("recent_run_ids", []) if r != run_id]
        profile["recent_run_ids"] = recent[:20]
        profile["last_task"] = task
        path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    except OSError:
        pass
