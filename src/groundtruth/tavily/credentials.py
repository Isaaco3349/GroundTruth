"""Resolve Tavily clients (API key or OAuth via Tavily CLI config)."""

from __future__ import annotations

from typing import Any

from groundtruth.config import get_settings


def get_tavily_client() -> Any:
    settings = get_settings()
    if settings.tavily_api_key.strip().startswith("tvly-"):
        from tavily import TavilyClient

        return TavilyClient(api_key=settings.tavily_api_key.strip())

    try:
        from tavily_cli.config import _build_keyed_client, get_api_key

        key = get_api_key()
        if key:
            return _build_keyed_client(key, client_name="groundtruth")
    except ImportError:
        pass

    if settings.tavily_api_key.strip():
        from tavily import TavilyClient

        return TavilyClient(api_key=settings.tavily_api_key.strip())

    raise RuntimeError(
        "No Tavily credential. Run tvly login or set a tvly API key in .env."
    )
