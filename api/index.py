"""Vercel serverless entry for the GroundTruth FastAPI app."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from groundtruth.api import app  # noqa: E402, F401
