from pydantic import BaseModel
import os

class Settings(BaseModel):
    livekit_api_key: str = os.getenv("LIVEKIT_API_KEY", "")
    livekit_api_secret: str = os.getenv("LIVEKIT_API_SECRET", "")
    livekit_url: str = os.getenv("LIVEKIT_URL", "")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY", "")

    cartesia_api_key: str = os.getenv("CARTESIA_API_KEY", "")

    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    allowed_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]


settings = Settings()
