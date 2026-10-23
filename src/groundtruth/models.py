from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ModelTier(str, Enum):
    nano = "nano"
    super = "super"
    ultra = "ultra"


class SourceCitation(BaseModel):
    url: str
    title: str = ""
    citation: str = ""


class EvidenceClaim(BaseModel):
    id: str
    text: str
    source_urls: list[str] = Field(default_factory=list)


class EvidencePack(BaseModel):
    query: str
    claims: list[EvidenceClaim] = Field(default_factory=list)
    sources: list[SourceCitation] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    raw: dict[str, Any] | None = None


class RunStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class RunRecord(BaseModel):
    id: str
    task: str
    status: RunStatus = RunStatus.pending
    model_events: list[dict[str, Any]] = Field(default_factory=list)
    evidence: EvidencePack | None = None
    summary: str = ""
