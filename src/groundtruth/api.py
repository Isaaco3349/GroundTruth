"""FastAPI surface for the web UI."""

import uuid

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

router = APIRouter(prefix="/api")


class RunRequest(BaseModel):
    task: str


@router.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "nemotron_configured": NemotronClient().is_configured(),
    }


@router.get("/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str) -> RunRecord:
    record = run_store.load(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return record


@router.post("/runs", response_model=RunRecord)
def create_run(body: RunRequest) -> RunRecord:
    run_id = str(uuid.uuid4())
    try:
        return run_task(body.task, run_id)
    except Exception as exc:
        from groundtruth.models import RunStatus

        return RunRecord(
            id=run_id,
            task=body.task,
            status=RunStatus.failed,
            summary=f"Server error: {exc}",
        )


app.include_router(router)
