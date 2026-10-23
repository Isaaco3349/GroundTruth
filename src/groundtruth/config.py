from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    nebius_api_key: str = ""
    nebius_base_url: str = "https://api.tokenfactory.nebius.com/v1/"
    nemotron_nano: str = "nvidia/nemotron-3-nano-30b-a3b"
    nemotron_super: str = "nvidia/nemotron-3-super-120b-a12b"
    nemotron_ultra: str = "nvidia/nemotron-3-ultra-550b-a55b"
    tavily_api_key: str = ""
    groundtruth_workspace: str = ""

    @property
    def workspace(self) -> Path:
        if self.groundtruth_workspace:
            return Path(self.groundtruth_workspace).resolve()
        return (ROOT / "fixtures" / "sample_project").resolve()


def get_settings() -> Settings:
    return Settings()
