import asyncio
from app.agents.agents_worker import _post_supabase

async def test_supabase():
    payload = {
        "call_id": "11111111-1111-1111-1111-111111111111",
        "sender": "agent",
        "content": "Hello world!"
    }
    await _post_supabase("messages", payload)

if __name__ == "__main__":
    asyncio.run(test_supabase())
