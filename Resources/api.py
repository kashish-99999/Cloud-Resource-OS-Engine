"""FastAPI endpoints for the Resources module (Banker's Algorithm).

Standalone run (project root se):
    uvicorn Resources.api:app --reload
Swagger UI: http://127.0.0.1:8000/docs

"""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

from Resources.allocator import ResourceAllocator
from Resources.deadlock import RequestResult
from Resources.graph import ResourceGraph

router = APIRouter(prefix="/resources", tags=["resources"])
DEFAULT_RESOURCES = ["CPU", "Memory", "IO"]
DEFAULT_TOTAL = [10, 5, 7]

allocator = ResourceAllocator(DEFAULT_RESOURCES, DEFAULT_TOTAL)



class InitBody(BaseModel):
    resource_names: list[str]
    total: list[int]

class ProcessBody(BaseModel):
    process_id: str
    max_demand: list[int]
    allocation: list[int] | None = None

class RequestBody(BaseModel):
    process_id: str
    request: list[int]

class ReleaseBody(BaseModel):
    process_id: str
    release: list[int] | None = None 


def _result_dict(result: RequestResult) -> dict:
    data = asdict(result)
    data["granted"] = result.granted
    return data


def _call(func, *args):
    """ValueError -> 400, KeyError -> 404."""
    try:
        return func(*args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Process not found: {exc}")

@router.post("/init")
def init_system(body: InitBody) -> dict:
    """Naya resource system banao (purana state clear)."""
    global allocator
    try:
        allocator = ResourceAllocator(body.resource_names, body.total)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return allocator.status()


@router.post("/process")
def register_process(body: ProcessBody) -> dict:
    _call(allocator.register_process, body.process_id, body.max_demand, body.allocation)
    return allocator.status()


@router.delete("/process/{process_id}")
def terminate_process(process_id: str) -> dict:
    granted = _call(allocator.terminate_process, process_id)
    return {"granted_from_wait": [_result_dict(r) for r in granted], "status": allocator.status()}

@router.post("/request")
def request_resources(body: RequestBody) -> dict:
    result = _call(allocator.request, body.process_id, body.request)
    return _result_dict(result)


@router.post("/release")
def release_resources(body: ReleaseBody) -> dict:
    granted = _call(allocator.release, body.process_id, body.release)
    return {"granted_from_wait": [_result_dict(r) for r in granted], "status": allocator.status()}


@router.get("/status")
def get_status() -> dict:
    return allocator.status()


@router.get("/safe-sequence")
def get_safe_sequence() -> dict:
    safety = allocator.banker.is_safe()
    return asdict(safety)


@router.get("/graph")
def get_graph(include_claims: bool = False) -> dict:
    return ResourceGraph(allocator).build_graph(include_claims)


@router.get("/deadlock")
def get_deadlock_status() -> dict:
    return ResourceGraph(allocator).deadlock_status()


@router.get("/events")
def get_events() -> list[dict]:
    return allocator.events

app = FastAPI(title="CROVME - Resource Management & Deadlock Avoidance")
app.include_router(router)