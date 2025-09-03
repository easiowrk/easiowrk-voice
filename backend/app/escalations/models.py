from __future__ import annotations
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class Escalation(BaseModel):
    id: UUID
    call_id: UUID
    issue: str
    status: Literal["pending", "resolved"]
    supervisor_response: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
