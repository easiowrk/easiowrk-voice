from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class EscalationCreate(BaseModel):
    call_id: UUID
    issue: str = Field(..., description="Reason the call was escalated")


class EscalationResponse(BaseModel):
    id: UUID
    call_id: UUID
    issue: str
    status: Literal["pending", "resolved"]
    supervisor_response: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class EscalationListResponse(BaseModel):
    items: list[EscalationResponse]
