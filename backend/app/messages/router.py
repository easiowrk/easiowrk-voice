from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

from app.messages.schemas import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
)
from app.messages.service import (
    create_message,
    list_messages_by_call,
    get_message,
)

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=MessageResponse, status_code=201)
def create_message_endpoint(body: MessageCreate):
    created = create_message(
        call_id=body.call_id,
        sender=body.sender,
        content=body.content,
        embedding=body.embedding,
    )
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create message")
    return created

@router.get("/", response_model=MessageListResponse)
def list_messages(
    call_id: UUID,
    limit: int = Query(default=200, ge=1, le=1000),
    ascending: bool = Query(default=True, description="True=oldest→newest, False=newest→oldest"),
):
    items = list_messages_by_call(call_id=call_id, limit=limit, ascending=ascending)
    return {"items": items}

@router.get("/{message_id}", response_model=MessageResponse)
def get_message_endpoint(message_id: UUID):
    msg = get_message(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
