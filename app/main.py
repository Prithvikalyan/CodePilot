
from fastapi import FastAPI

from app.api.routes import router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="CodePilot",
    description="AI Project Analyst Agent",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CodePilot!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
