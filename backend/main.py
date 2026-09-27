from fastapi import FastAPI

app = FastAPI(
    title="NammaSahay AI",
    description="Tamil-first AI assistant for public services and government schemes",
    version="0.1.0",
)


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
