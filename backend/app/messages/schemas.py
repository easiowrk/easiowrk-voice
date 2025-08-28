from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal, Annotated, List
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints, ConfigDict

Sender = Literal["agent", "customer", "supervisor"]

# Soft length guard to avoid massive payloads
SmallText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=8000)]

class MessageCreate(BaseModel):
    call_id: UUID
    sender: Sender
    content: SmallText = Field(..., description="Raw transcript text")
    embedding: Optional[list[float]] = Field(default=None, description="Optional 1536-d vector")

class MessageResponse(BaseModel):
    id: UUID
    call_id: UUID
    sender: Sender
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageListResponse(BaseModel):
    items: List[MessageResponse]
