import os
import shutil
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


def is_vercel() -> bool:
    return bool(os.getenv("VERCEL"))


def runtime_data_dir() -> Path:
    if is_vercel():
        path = Path("/tmp/groundtruth_data")
        path.mkdir(parents=True, exist_ok=True)
        return path
    return ROOT / "data"


def prepare_workspace(workspace: Path) -> Path:
    """Copy sample fixture to /tmp on Vercel (read only deployment filesystem)."""
    if not is_vercel():
        return workspace
    src = ROOT / "fixtures" / "sample_project"
    target = Path("/tmp/groundtruth_sample")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target)
    return target


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
        if is_vercel():
            return Path("/tmp/groundtruth_sample")
        return (ROOT / "fixtures" / "sample_project").resolve()


def get_settings() -> Settings:
    return Settings()
