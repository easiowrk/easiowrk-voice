from __future__ import annotations
from typing import List, Optional
from uuid import UUID, uuid4

from app.core.database import supabase

TABLE = "messages"

def create_message(
    *,
    call_id: UUID,
    sender: str,
    content: str,
    embedding: Optional[list[float]] = None,
) -> dict:
    message_id = uuid4()
    payload = {
        "id": str(message_id),
        "call_id": str(call_id),
        "sender": sender,
        "content": content,
    }
    if embedding is not None:
        # Supabase Python client will serialize list[float] to PostgREST; pgvector accepts arrays.
        payload["embedding"] = embedding

    res = supabase.table(TABLE).insert(payload).execute()
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase insert error: {res.error}")

    fetched = (
        supabase.table(TABLE)
        .select("id,call_id,sender,content,created_at")
        .eq("id", str(message_id))
        .single()
        .execute()
    )
    if getattr(fetched, "error", None):
        raise RuntimeError(f"Supabase fetch-after-insert error: {fetched.error}")

    data = getattr(fetched, "data", None)
    if not data:
        raise RuntimeError("Insert succeeded but no row was returned on fetch.")
    return data

def list_messages_by_call(
    *,
    call_id: UUID,
    limit: int = 200,
    ascending: bool = True,
) -> List[dict]:
    order_asc = not (ascending is False)
    q = (
        supabase.table(TABLE)
        .select("id,call_id,sender,content,created_at")
        .eq("call_id", str(call_id))
        .order("created_at", desc=not order_asc)
        .limit(limit)
    )
    res = q.execute()
    return getattr(res, "data", None) or []

def get_message(message_id: UUID) -> Optional[dict]:
    res = (
        supabase.table(TABLE)
        .select("id,call_id,sender,content,created_at")
        .eq("id", str(message_id))
        .single()
        .execute()
    )
    return getattr(res, "data", None)
