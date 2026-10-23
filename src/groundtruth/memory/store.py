"""Local memory for stack notes and recent runs."""

from __future__ import annotations

import json
from pathlib import Path

from groundtruth.config import ROOT

MEMORY_PATH = ROOT / "data" / "memory" / "profile.json"


def load_profile() -> dict:
    if not MEMORY_PATH.is_file():
        return {"notes": [], "recent_run_ids": []}
    return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))


def remember_run(run_id: str, task: str) -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    profile = load_profile()
    recent = [run_id] + [r for r in profile.get("recent_run_ids", []) if r != run_id]
    profile["recent_run_ids"] = recent[:20]
    profile["last_task"] = task
    MEMORY_PATH.write_text(json.dumps(profile, indent=2), encoding="utf-8")
