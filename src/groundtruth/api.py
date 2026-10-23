"""FastAPI surface for the web UI."""

import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi import HTTPException

from groundtruth.agent.loop import run_task
from groundtruth.models import RunRecord
from groundtruth.nemotron.client import NemotronClient
from groundtruth.runs import store as run_store

app = FastAPI(title="GroundTruth API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    task: str


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "nemotron_configured": NemotronClient().is_configured(),
    }


@app.get("/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str) -> RunRecord:
    record = run_store.load(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return record


@app.post("/runs", response_model=RunRecord)
def create_run(body: RunRequest) -> RunRecord:
    run_id = str(uuid.uuid4())
    return run_task(body.task, run_id)
