from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints, ConfigDict

Direction = Literal["inbound", "outbound"]
Status = Literal["active", "completed", "failed"]

Phone = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=7,
        max_length=20,
        pattern=r"^\+?[0-9]{7,20}$",
    ),
]

class CallCreate(BaseModel):
    agent_id: Optional[UUID]
    customer_number: Phone = Field(..., description="Caller/callee number (prefer E.164, e.g., +2348012345678)")
    direction: Direction

class CallResponse(BaseModel):
    id: UUID
    agent_id: Optional[UUID]
    customer_number: Phone
    direction: Direction
    status: Status
    started_at: datetime
    ended_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
