"""Agent orchestration loop."""

from __future__ import annotations

import time
from typing import Any

from groundtruth.agent.planner import plan_patch
from groundtruth.config import get_settings, is_vercel, prepare_workspace
from groundtruth.memory.store import remember_run
from groundtruth.models import EvidencePack, ModelTier, RunRecord, RunStatus
from groundtruth.nemotron.client import NemotronClient
from groundtruth.runs import store as run_store
from groundtruth.tavily.fetch import load_evidence
from groundtruth.tools import workspace as ws


def _log(record: RunRecord, message: str, **extra: Any) -> None:
    entry: dict[str, Any] = {"t": time.time(), "message": message, **extra}
    record.model_events.append(entry)


def _evidence_ok(pack: EvidencePack) -> bool:
    return bool(pack.sources or pack.claims)


def run_task(task: str, run_id: str) -> RunRecord:
    settings = get_settings()
    workspace = prepare_workspace(settings.workspace)
    record = RunRecord(id=run_id, task=task, status=RunStatus.running)
    client = NemotronClient(settings)

    _log(
        record,
        "Run started",
        workspace=str(workspace),
        nemotron_configured=client.is_configured(),
    )

    if ws.reset_sample_bug(workspace):
        _log(record, "Reset sample fixture to failing state")

    evidence_query = f"Context for software task: {task}"
    try:
        evidence = load_evidence(evidence_query, task)
        record.evidence = evidence
        mode = (
            "bundled-demo"
            if (evidence.raw or {}).get("mode") == "demo"
            else "tavily"
        )
        _log(
            record,
            "Tavily evidence loaded",
            sources=len(evidence.sources),
            claims=len(evidence.claims),
            mode=mode,
        )
    except Exception as exc:
        _log(record, "Tavily failed", error=str(exc))
        record.status = RunStatus.failed
        record.summary = f"Tavily error: {exc}"
        run_store.save(record)
        return record

    if not _evidence_ok(evidence):
        record.status = RunStatus.failed
        record.summary = "Evidence gate blocked run: no claims or sources from Tavily."
        _log(record, record.summary)
        run_store.save(record)
        return record

    snippets: dict[str, str] = {}
    for rel in ("sampledemo/__init__.py", "tests/test_greet.py"):
        try:
            snippets[rel] = ws.read_text_file(workspace, rel)
        except OSError:
            pass

    try:
        patch, tier = plan_patch(workspace, task, evidence, snippets, client=client)
        _log(
            record,
            "Patch planned",
            relative_path=patch["relative_path"],
            tier=tier.value if tier else "fallback",
        )
    except Exception as exc:
        record.status = RunStatus.failed
        record.summary = f"Planning failed: {exc}"
        _log(record, record.summary)
        run_store.save(record)
        return record

    try:
        ws.write_text_file(workspace, patch["relative_path"], patch["content"])
        _log(record, "Patch applied", relative_path=patch["relative_path"])
    except Exception as exc:
        record.status = RunStatus.failed
        record.summary = f"Write failed: {exc}"
        run_store.save(record)
        return record

    code, test_output = ws.run_tests(workspace, prefer_pytest=not is_vercel())
    _log(
        record,
        "Verification finished",
        exit_code=code,
        mode="inline" if is_vercel() else "pytest",
        output=test_output[-4000:],
    )

    if code == 0:
        record.status = RunStatus.completed
        if tier:
            tier_note = tier.value
        else:
            tier_note = "fallback (Nemotron auth failed or not configured; sample path only)"
        record.summary = (
            f"Tests passed. Model tier: {tier_note}. "
            f"Evidence: {len(evidence.sources)} sources, {len(evidence.claims)} claims."
        )
        remember_run(run_id, task)
    else:
        record.status = RunStatus.failed
        record.summary = f"Tests failed after patch.\n{test_output[-1500:]}"

    run_store.save(record)
    return record
