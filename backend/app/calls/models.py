from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class Call(BaseModel):
    id: UUID
    agent_id: Optional[UUID]
    customer_number: str
    direction: Literal["inbound", "outbound"]
    status: Literal["active", "completed", "failed"]
    started_at: datetime
    ended_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
