"""Resolve Tavily clients (API key or OAuth via Tavily CLI config)."""

from __future__ import annotations

from typing import Any

from groundtruth.config import get_settings, is_vercel


def get_tavily_client() -> Any:
    settings = get_settings()
    key = settings.tavily_api_key.strip()
    if key:
        from tavily import TavilyClient

        return TavilyClient(api_key=key)

    if is_vercel():
        raise RuntimeError("Set TAVILY_API_KEY on Vercel (tvly-… from the dashboard).")

    try:
        from tavily_cli.config import _build_keyed_client, get_api_key

        oauth = get_api_key()
        if oauth:
            return _build_keyed_client(oauth, client_name="groundtruth")
    except ImportError:
        pass

    raise RuntimeError(
        "No Tavily credential. Run tvly login or set a tvly API key in .env."
    )
