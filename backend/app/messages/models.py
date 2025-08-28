from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class Message(BaseModel):
    id: UUID
    call_id: UUID
    sender: Literal["agent", "customer", "supervisor"]
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
