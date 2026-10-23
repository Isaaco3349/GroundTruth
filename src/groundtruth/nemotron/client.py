"""Nebius Token Factory client wrapper."""

from __future__ import annotations

from openai import OpenAI

from groundtruth.config import Settings, get_settings
from groundtruth.models import ModelTier


class NemotronClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: OpenAI | None = None

    def is_configured(self) -> bool:
        return bool(self.settings.nebius_api_key.strip())

    def _openai(self) -> OpenAI:
        if not self.is_configured():
            raise RuntimeError(
                "NEBIUS_API_KEY is not set. Waiting for Token Factory access. "
                "Fallback planner will run if enabled."
            )
        if self._client is None:
            self._client = OpenAI(
                base_url=self.settings.nebius_base_url,
                api_key=self.settings.nebius_api_key,
            )
        return self._client

    def model_id(self, tier: ModelTier) -> str:
        if tier == ModelTier.nano:
            return self.settings.nemotron_nano
        if tier == ModelTier.ultra:
            return self.settings.nemotron_ultra
        return self.settings.nemotron_super

    def complete(self, tier: ModelTier, system: str, user: str) -> str:
        response = self._openai().chat.completions.create(
            model=self.model_id(tier),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )
        choice = response.choices[0].message.content
        return choice or ""
