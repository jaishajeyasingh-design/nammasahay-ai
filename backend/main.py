from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat_router

app = FastAPI(
    title="NammaSahay AI",
    description="Tamil-first AI assistant for public services and government schemes",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to NammaSahay AI 🇮🇳",
        "status": "Backend is running",
    }


@app.get("/health")
def check_health() -> dict[str, str]:
    return {
        "status": "healthy",
    }

