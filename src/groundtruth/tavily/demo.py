"""Bundled evidence for fast Vercel demo when live Tavily is slow."""

from __future__ import annotations

import json

from groundtruth.config import ROOT
from groundtruth.models import EvidenceClaim, EvidencePack, SourceCitation

DEMO_PATH = ROOT / "fixtures" / "demo_evidence.json"

INLINE_DEMO = EvidencePack(
    query="Context for software task: Fix the failing test in the sample project",
    claims=[
        EvidenceClaim(
            id="1",
            text="Failing tests should be reproduced, fixed, and re-run until green before merge.",
            source_urls=["https://docs.pytest.org/en/stable/how-to/assert.html"],
        )
    ],
    sources=[
        SourceCitation(
            url="https://docs.pytest.org/en/stable/how-to/assert.html",
            title="pytest assertions",
            citation="pytest documentation",
        ),
        SourceCitation(
            url="https://undo.io/resources/what-to-do-about-failing-tests",
            title="What to do about failing tests",
            citation="Undo",
        ),
    ],
    risks=[],
    raw={"mode": "demo"},
)


def demo_evidence_for_task(task: str) -> EvidencePack | None:
    if "fix the failing test" not in task.lower():
        return None
    if DEMO_PATH.is_file():
        data = json.loads(DEMO_PATH.read_text(encoding="utf-8"))
        pack = EvidencePack.model_validate(data)
        pack.raw = {"mode": "demo"}
        return pack
    return INLINE_DEMO.model_copy(deep=True)
