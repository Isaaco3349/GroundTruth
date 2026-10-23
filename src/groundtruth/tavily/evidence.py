"""Tavily Research and Search helpers for EvidencePack."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from groundtruth.config import ROOT
from groundtruth.models import EvidenceClaim, EvidencePack, SourceCitation
from groundtruth.tavily.credentials import get_tavily_client

CACHE_DIR = ROOT / "data" / "evidence_cache"

EVIDENCE_SCHEMA: dict[str, Any] = {
    "properties": {
        "claims": {
            "type": "array",
            "description": "Factual claims supported by sources",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                    "source_urls": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["id", "text"],
            },
        },
        "risks": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Uncertainties or breaking change risks",
        },
    },
    "required": ["claims"],
}


def _client():
    return get_tavily_client()


def _cache_path(query: str, mode: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(f"{mode}:{query}".encode()).hexdigest()[:16]
    return CACHE_DIR / f"{digest}.json"


def _load_cache(path: Path) -> EvidencePack | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return EvidencePack.model_validate(data)
    except (json.JSONDecodeError, ValueError):
        return None


def _save_cache(path: Path, pack: EvidencePack) -> None:
    path.write_text(pack.model_dump_json(indent=2), encoding="utf-8")


def _pack_from_research_response(query: str, response: dict[str, Any]) -> EvidencePack:
    sources = [
        SourceCitation(
            url=s.get("url", ""),
            title=s.get("title", "") or "",
            citation=s.get("citation", "") or "",
        )
        for s in response.get("sources", []) or []
        if s.get("url")
    ]
    structured = response.get("structured_output") or response.get("content")
    claims: list[EvidenceClaim] = []
    risks: list[str] = []

    if isinstance(structured, dict):
        for item in structured.get("claims", []) or []:
            claims.append(
                EvidenceClaim(
                    id=str(item.get("id", len(claims) + 1)),
                    text=str(item.get("text", "")),
                    source_urls=list(item.get("source_urls") or []),
                )
            )
        risks = [str(r) for r in structured.get("risks") or []]
    elif isinstance(structured, str) and structured.strip():
        claims.append(EvidenceClaim(id="1", text=structured.strip()[:2000], source_urls=[]))

    return EvidencePack(
        query=query,
        claims=claims,
        sources=sources,
        risks=risks,
        raw={"status": response.get("status"), "request_id": response.get("request_id")},
    )


def _pack_from_search(query: str, response: dict[str, Any]) -> EvidencePack:
    sources: list[SourceCitation] = []
    claims: list[EvidenceClaim] = []
    for idx, result in enumerate(response.get("results") or [], start=1):
        url = result.get("url", "")
        title = result.get("title", "") or url
        snippet = result.get("content", "") or result.get("raw_content", "") or ""
        if url:
            sources.append(SourceCitation(url=url, title=title, citation=title))
        if snippet:
            claims.append(
                EvidenceClaim(
                    id=str(idx),
                    text=snippet[:500],
                    source_urls=[url] if url else [],
                )
            )
    return EvidencePack(query=query, claims=claims, sources=sources, risks=[], raw={"mode": "search"})


def fetch_evidence(query: str, use_research: bool = True, use_cache: bool = True) -> EvidencePack:
    mode = "research" if use_research else "search"
    cache = _cache_path(query, mode)
    if use_cache:
        cached = _load_cache(cache)
        if cached is not None:
            return cached

    client = _client()
    if use_research:
        started = client.research(
            input=query,
            model="mini",
            output_schema=EVIDENCE_SCHEMA,
            citation_format="numbered",
        )
        request_id = started.get("request_id")
        if not request_id:
            raise RuntimeError("Tavily research did not return request_id")

        deadline = time.time() + 120
        response: dict[str, Any] = {"status": "pending"}
        while time.time() < deadline:
            response = client.get_research(request_id)
            status = response.get("status")
            if status in ("completed", "failed"):
                break
            time.sleep(2)

        if response.get("status") == "failed":
            pack = EvidencePack(
                query=query,
                claims=[],
                sources=[],
                risks=["Tavily research failed"],
                raw=response,
            )
        else:
            pack = _pack_from_research_response(query, response)
    else:
        response = client.search(
            query=query[:400],
            search_depth="advanced",
            max_results=5,
        )
        pack = _pack_from_search(query, response)

    if use_cache:
        _save_cache(cache, pack)
    return pack
