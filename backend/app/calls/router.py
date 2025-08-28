from __future__ import annotations
from typing import Optional, List
from uuid import UUID
import asyncio

from fastapi import APIRouter, HTTPException, Query

from app.calls.service import create_call, get_calls, get_call, complete_call, create_agent_token
from app.calls.schemas import CallCreate, CallResponse
from app.agents.service import start_agent_session

router = APIRouter(prefix="/calls", tags=["Calls"])

@router.post("/", response_model=CallResponse, status_code=201)
def create_call_endpoint(call: CallCreate):
    created = create_call(call.agent_id, call.customer_number, call.direction)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create call")
    return created

@router.get("/", response_model=List[CallResponse])
def list_calls(
    limit: int = Query(default=50, ge=1, le=200),
    agent_id: Optional[UUID] = None,
    status: Optional[str] = Query(default=None, pattern="^(active|completed|failed)$")
):
    return get_calls(limit=limit, agent_id=agent_id, status=status)

@router.get("/{call_id}", response_model=CallResponse)
def get_call_endpoint(call_id: UUID):
    call = get_call(call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.post("/{call_id}/complete", response_model=CallResponse)
def complete_call_endpoint(call_id: UUID):
    updated = complete_call(call_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Call not found or update failed")
    return updated


@router.post("/start")
async def start_call(
    room_name: str = Query(..., description="Name of the LiveKit room"),
    identity: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
):

    try:
        token = create_agent_token(room_name, identity)
        if agent_id:
            asyncio.create_task(start_agent_session(agent_id, room_name))
        return {"room": room_name, "token": token, "identity": identity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))