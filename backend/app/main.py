from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
from app.calls.router import router as calls_router
from app.messages.router import router as messages_router
from app.escalations.router import router as escalations_router

# from app.slack.router import router as slack_router


app = FastAPI(title="EasioWrk")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.allowed_origins, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


app.include_router(calls_router)
app.include_router(messages_router)
app.include_router(escalations_router)
# app.include_router(slack_router)



@app.get("/")
def root():
    return {"message": "AI Voice Agent Backend Running 🚀"}
