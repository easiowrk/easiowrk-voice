from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

from app.calls.service import (
    create_call,
    get_calls,
    get_call,
    complete_call,
    create_agent_token,
)
from app.calls.schemas import CallCreate, CallResponse

router = APIRouter()

router = APIRouter(prefix="/calls", tags=["Calls"])

@router.post("/", response_model=CallResponse, status_code=201)
def create_call_endpoint(call: CallCreate):
    created = create_call(call.agent_id, call.customer_number, call.direction)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create call")
    return created


@router.get("/", response_model=list[CallResponse])
def list_calls(
    limit: int = Query(default=50, ge=1, le=200),
    agent_id: UUID | None = None,
    status: str | None = Query(default=None, pattern="^(active|completed|failed)$"),
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
    customer_number: str = Query(..., description="Customer’s number or ID"),
    identity: str | None = Query(default=None, description="Customer identity for LiveKit"),
):
    """
    Start a call: creates a call record + LiveKit token.
    Worker auto-joins independently.
    """
    try:
        call = create_call(agent_id=None, customer_number=customer_number, direction="inbound")
        if not call or "id" not in call:
            raise RuntimeError("Failed to create call")

        call_id = UUID(call["id"])
        room_name = str(call_id)

        token = create_agent_token(room_name, identity)

        return {
            "call_id": str(call_id),
            "room": room_name,
            "token": token,
            "identity": identity,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
