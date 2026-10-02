import os
import sys
from pathlib import Path

# Ensure backend folder is in Python path for Vercel serverless runtime
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat_router

app = FastAPI(
    title="NammaSahay AI",
    description="Tamil-first AI assistant for public services and government schemes",
    version="0.1.0",
)

allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
