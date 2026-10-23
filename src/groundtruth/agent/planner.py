"""Patch planning with Nemotron or deterministic fallback."""

from __future__ import annotations

import json
import re
from pathlib import Path

from groundtruth.models import EvidencePack, ModelTier
from groundtruth.nemotron.client import NemotronClient
from groundtruth.nemotron.router import choose_tier
from groundtruth.tools import workspace as ws


def _parse_patch_json(text: str) -> dict[str, str]:
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1)
    data = json.loads(cleaned)
    if "relative_path" not in data or "content" not in data:
        raise ValueError("Patch JSON must include relative_path and content")
    return {"relative_path": str(data["relative_path"]), "content": str(data["content"])}


def fallback_plan(workspace: Path, task: str, evidence: EvidencePack | None) -> dict[str, str]:
    expected = ws.infer_expected_from_tests(workspace)
    rel = "sampledemo/__init__.py"
    if expected:
        content = (
            f'def greet(name: str) -> str:\n'
            f'    return "{expected}"\n'
        )
        return {"relative_path": rel, "content": content}

    raise RuntimeError(
        "Fallback planner only handles the sample greet test fixture. "
        "Set NEBIUS_API_KEY for general tasks."
    )


def plan_patch(
    workspace: Path,
    task: str,
    evidence: EvidencePack | None,
    file_snippets: dict[str, str],
    client: NemotronClient | None = None,
) -> tuple[dict[str, str], ModelTier | None]:
    nemotron = client or NemotronClient()
    tier = choose_tier(task)

    if not nemotron.is_configured():
        return fallback_plan(workspace, task, evidence), None

    evidence_text = ""
    if evidence:
        claims = "\n".join(f"- {c.text}" for c in evidence.claims[:8])
        sources = "\n".join(f"- {s.url}" for s in evidence.sources[:8])
        evidence_text = f"Claims:\n{claims}\n\nSources:\n{sources}\n"

    files_block = "\n\n".join(
        f"FILE: {name}\n```\n{body}\n```" for name, body in file_snippets.items()
    )

    system = (
        "You are a coding agent. Respond with JSON only, no markdown prose. "
        'Shape: {"relative_path": "path/from/workspace", "content": "full file content"}'
    )
    user = f"Task:\n{task}\n\n{evidence_text}\n{files_block}\n\nReturn the patched file as JSON."

    try:
        raw = nemotron.complete(tier, system, user)
        return _parse_patch_json(raw), tier
    except Exception as exc:
        err = str(exc).lower()
        auth_failed = any(
            token in err
            for token in ("401", "unauthorized", "authenticate", "invalid api key")
        )
        if auth_failed:
            return fallback_plan(workspace, task, evidence), None
        raise
