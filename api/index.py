"""Vercel FastAPI entrypoint (api service)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from groundtruth.api import app  # noqa: E402
