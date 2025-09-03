from __future__ import annotations
from livekit import api
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.core.config import settings
from app.core.database import supabase

TABLE = "calls"

def create_agent_token(room_name: str, identity: str | None = None) -> str:
    identity = identity or f"web-{uuid4()}"
    token = (
        api.AccessToken(
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
        )
        .with_identity(identity)
        .with_name(identity)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )
    return token


def _fetch_call_by_id(call_id: UUID) -> Optional[dict]:
    res = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", str(call_id))
        .single()
        .execute()
    )
    return getattr(res, "data", None)


def create_call(agent_id: Optional[UUID], customer_number: str, direction: str = "outbound") -> dict:
    call_id = uuid4()
    payload = {
        "id": str(call_id),
        "agent_id": str(agent_id) if agent_id else None,
        "customer_number": customer_number,
        "direction": direction,
        "status": "active",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }

    res = supabase.table(TABLE).insert(payload).execute()
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase insert error: {res.error}")

    row = _fetch_call_by_id(call_id)
    if not row:
        raise RuntimeError("Insert succeeded but no row was returned on fetch.")
    return row


def get_calls(
    *,
    limit: int = 50,
    agent_id: Optional[UUID] = None,
    status: Optional[str] = None,
) -> List[dict]:
    q = supabase.table(TABLE).select("*").order("started_at", desc=True).limit(limit)
    if agent_id:
        q = q.eq("agent_id", str(agent_id))
    if status:
        q = q.eq("status", status)

    res = q.execute()
    return getattr(res, "data", None) or []


def get_call(call_id: UUID) -> Optional[dict]:
    return _fetch_call_by_id(call_id)


def complete_call(call_id: UUID) -> Optional[dict]:
    updates = {
        "status": "completed",
        "ended_at": datetime.now(timezone.utc).isoformat(),
    }

    res = supabase.table(TABLE).update(updates).eq("id", str(call_id)).execute()
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase update error: {res.error}")

    row = _fetch_call_by_id(call_id)
    return row


# 🔑 NEW: tell LiveKit to spin up the agent-worker
def dispatch_agent_job(call_id: UUID, room_name: str, agent_identity: str):
    lk = api.LiveKitAPI(
        settings.livekit_api_key,
        settings.livekit_api_secret,
        settings.livekit_host,  # e.g. "https://<your-domain>.livekit.cloud"
    )

    job_req = api.AgentJobRequest(
        worker_name="agent-worker",   # must match the worker registered in `agents_worker.py`
        room_name=room_name,
        identity=agent_identity,
        metadata={"call_id": str(call_id)},
    )

    lk.agents.create_job(job_req)
    print(f"🚀 Dispatched agent job for call {call_id} in room {room_name}")
