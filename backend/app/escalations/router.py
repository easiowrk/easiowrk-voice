from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.escalations.service import (
    create_escalation,
    resolve_escalation,
    list_escalations,
    get_escalation,
)
from app.escalations.schemas import EscalationCreate, EscalationResponse

router = APIRouter(prefix="/escalations", tags=["Escalations"])


@router.post("/", response_model=EscalationResponse, status_code=201)
def create_escalation_endpoint(body: EscalationCreate):
    created = create_escalation(body.call_id, body.issue)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create escalation")
    return created


@router.get("/", response_model=List[EscalationResponse])
def list_escalations_endpoint(call_id: UUID = Query(..., description="Filter by call_id")):
    items = list_escalations(call_id)
    return items


@router.get("/{escalation_id}", response_model=EscalationResponse)
def get_escalation_endpoint(escalation_id: UUID):
    esc = get_escalation(escalation_id)
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return esc


@router.patch("/{escalation_id}/resolve", response_model=EscalationResponse)
def resolve_escalation_endpoint(escalation_id: UUID, supervisor_response: Optional[str] = None):
    updated = resolve_escalation(escalation_id, supervisor_response)
    if not updated:
        raise HTTPException(status_code=404, detail="Escalation not found or update failed")
    return updated
