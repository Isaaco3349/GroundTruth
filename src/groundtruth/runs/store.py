"""Persist run records for API and UI."""

from __future__ import annotations

import json
from pathlib import Path

from groundtruth.config import runtime_data_dir
from groundtruth.models import RunRecord


def runs_dir() -> Path:
    path = runtime_data_dir() / "runs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save(record: RunRecord) -> None:
    path = runs_dir() / f"{record.id}.json"
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")


def load(run_id: str) -> RunRecord | None:
    path = runs_dir() / f"{run_id}.json"
    if not path.is_file():
        return None
    return RunRecord.model_validate(json.loads(path.read_text(encoding="utf-8")))
