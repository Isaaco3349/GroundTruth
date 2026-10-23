"""Persist run records for API and UI."""

from __future__ import annotations

import json
from pathlib import Path

from groundtruth.config import ROOT
from groundtruth.models import RunRecord

RUNS_DIR = ROOT / "data" / "runs"


def save(record: RunRecord) -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / f"{record.id}.json"
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")


def load(run_id: str) -> RunRecord | None:
    path = RUNS_DIR / f"{run_id}.json"
    if not path.is_file():
        return None
    return RunRecord.model_validate(json.loads(path.read_text(encoding="utf-8")))
