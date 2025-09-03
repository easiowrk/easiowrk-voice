import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import httpx
import asyncio

from livekit.agents import (
    AgentSession,
    Agent,
    RoomInputOptions,
    WorkerOptions,
    JobContext,
    cli,
    UserInputTranscribedEvent,
    ConversationItemAddedEvent,
)
from livekit.plugins import deepgram, openai, cartesia, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ---------------------------------------------------------------------------
# Helpers to post into Supabase
# ---------------------------------------------------------------------------

async def _post_supabase(table: str, payload: dict):
    if not (SUPABASE_URL and SUPABASE_KEY):
        print("[supabase] URL/KEY missing")
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{SUPABASE_URL}/rest/v1/{table}",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation",  # show response
                },
                json=payload,
            )
            if r.status_code >= 300:
                print(f"[supabase error] {r.status_code}: {r.text}")
            else:
                print(f"[supabase ok] {table} <- {payload}")
    except Exception as e:
        print(f"[supabase exception] {e}")


async def log_message(call_id: str, sender: str, content: str):
    if not content.strip():
        return

    # Generate embedding before saving
    emb = None
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={"model": "text-embedding-3-small", "input": content},
                )
                resp.raise_for_status()
                emb = resp.json()["data"][0]["embedding"]
    except Exception as e:
        print(f"[embedding error] {e}")

    payload = {
        "call_id": call_id,
        "sender": sender,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if emb:
        payload["embedding"] = emb

    # Save to Supabase
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{SUPABASE_URL}/rest/v1/messages",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation",
                },
                json=payload,
            )
            if r.status_code >= 300:
                print(f"[supabase error] {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[supabase insert error] {e}")


async def log_escalation(call_id: str, issue: str):
    await _post_supabase(
        "escalations",
        {
            "call_id": call_id,
            "issue": issue,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# Main agent entry
# ---------------------------------------------------------------------------

async def agent_entry(job: JobContext):
    room = job.room
    call_id = room.name  # your room == call_id
    import json
    try:
        meta = json.loads(room.metadata or "{}")
    except Exception:
        meta = {}

    # Pick up customer_number from metadata - Hardcoded it in frontend
    customer_number = meta.get("customer_number", "unknown")

    # --- Ensure call is registered in Supabase -------------------------------
    await _post_supabase("calls", {
        "id": call_id,
        "agent_id": None,
        "customer_number": customer_number,
        "direction": "inbound",
        "status": "active",
        "started_at": datetime.now(timezone.utc).isoformat(),
    })

    # --- Models --------------------------------------------------------------
    stt = deepgram.STT(
        model="nova-3",
        language="multi",
        api_key=os.getenv("DEEPGRAM_API_KEY"),
    )

    llm = openai.LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Cartesia TTS
    tts_model = os.getenv("CARTESIA_TTS_MODEL", "sonic-2")
    voice_id = os.getenv("CARTESIA_VOICE_ID")
    tts_kwargs = dict(api_key=os.getenv("CARTESIA_API_KEY"), model=tts_model, voice=voice_id)

    speed_env = os.getenv("TTS_SPEED")
    if speed_env and tts_model == "sonic-2-2025-03-07":
        tts_kwargs["speed"] = float(speed_env)

    tts = cartesia.TTS(**tts_kwargs)

    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # --- Persist transcripts & agent messages --------------------------------
    @session.on("user_input_transcribed")
    def _on_user_transcribed(ev: UserInputTranscribedEvent):
        if ev.is_final and ev.transcript.strip():
            asyncio.create_task(log_message(call_id, "customer", ev.transcript))

    @session.on("conversation_item_added")
    def _on_item_added(ev: ConversationItemAddedEvent):
        role = ev.item.role  # "assistant" or "user"
        text = ev.item.text_content or ""
        if text.strip():
            sender = "agent" if role == "assistant" else "customer"
            asyncio.create_task(log_message(call_id, sender, text))
            if sender == "agent" and "escalate" in text.lower():
                asyncio.create_task(log_escalation(call_id, text))

    # --- Start and greet ------------------------------------------------------
    await session.start(
        room=room,
        agent=Agent(
            instructions=(
                "You are a friendly customer support agent. "
                "Speak in short, clear sentences suitable for phone calls. "
                "Do NOT use markdown, asterisks, lists, or emoji. "
                "Confirm understanding and keep responses concise."
            )
        ),
        room_input_options=RoomInputOptions(close_on_disconnect=True),
    )

    await session.say(text="Hi! This is EasioWork Call Center. How can I help you today?")

    try:
        async for _ in session.run(user_input=job.user_input):
            pass
    finally:
        # --- Mark call completed ---------------------------------------------
        await _post_supabase("calls", {
            "id": call_id,
            "status": "completed",
            "ended_at": datetime.now(timezone.utc).isoformat(),
        })


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=agent_entry))
