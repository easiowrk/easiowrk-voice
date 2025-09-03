from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, List
from app.core.database import supabase

TABLE = "escalations"


def _fetch_by_id(escalation_id: UUID) -> Optional[dict]:
    res = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", str(escalation_id))
        .single()
        .execute()
    )
    return getattr(res, "data", None)


def create_escalation(call_id: UUID, issue: str) -> dict:
    """
    Insert, then fetch to return a complete, typed row.
    """
    escalation_id = uuid4()
    payload = {
        "id": str(escalation_id),
        "call_id": str(call_id),
        "issue": issue,
        "status": "pending",
    }
    res = supabase.table(TABLE).insert(payload).execute()
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase insert error: {res.error}")

    row = _fetch_by_id(escalation_id)
    if not row:
        raise RuntimeError("Insert succeeded but no row was returned on fetch.")
    return row


def resolve_escalation(escalation_id: UUID, supervisor_response: Optional[str] = None) -> dict:
    """
    Update, then fetch to return a complete, typed row.
    """
    updates = {
        "status": "resolved",
        "supervisor_response": supervisor_response,
        "resolved_at": datetime.now(timezone.utc).isoformat(),
    }
    res = (
        supabase.table(TABLE)
        .update(updates)
        .eq("id", str(escalation_id))
        .execute()
    )
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase update error: {res.error}")

    row = _fetch_by_id(escalation_id)
    if not row:
        raise RuntimeError("Update succeeded but no row was returned on fetch.")
    return row


def list_escalations(call_id: Optional[UUID] = None) -> List[dict]:
    """
    Make call_id optional so /escalations can list all or filter by call.
    """
    q = supabase.table(TABLE).select("*").order("created_at", desc=True)
    if call_id:
        q = q.eq("call_id", str(call_id))
    res = q.execute()
    return getattr(res, "data", None) or []


def get_escalation(escalation_id: UUID) -> Optional[dict]:
    return _fetch_by_id(escalation_id)
