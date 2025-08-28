from pydantic import BaseModel
import os

class Settings(BaseModel):
    livekit_api_key: str = os.getenv("LIVEKIT_API_KEY", "")
    livekit_api_secret: str = os.getenv("LIVEKIT_API_SECRET", "")
    livekit_url: str = os.getenv("LIVEKIT_URL", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    allowed_origins: list[str] = (os.getenv("ALLOWED_ORIGINS","http://localhost:3000").split(","))

settings = Settings()
