"""Fetch evidence with optional timeout (serverless friendly)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

from groundtruth.config import is_vercel
from groundtruth.models import EvidencePack
from groundtruth.tavily.demo import demo_evidence_for_task
from groundtruth.tavily.evidence import fetch_evidence


def load_evidence(query: str, task: str) -> EvidencePack:
    demo = demo_evidence_for_task(task)
    if is_vercel() and demo is not None:
        return demo

    use_research = not is_vercel() and any(
        k in task.lower() for k in ("api", "library", "migrate")
    )

    def _call() -> EvidencePack:
        return fetch_evidence(
            query,
            use_research=use_research,
            use_cache=True,
        )

    timeout = 20 if is_vercel() else 120
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_call)
        try:
            return future.result(timeout=timeout)
        except (FuturesTimeout, Exception):
            if demo is not None:
                return demo
            raise
