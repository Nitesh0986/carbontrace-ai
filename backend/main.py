"""
CarbonTrace AI
FastAPI Application
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router


app = FastAPI(
    title="CarbonTrace AI",
    description=(
        "AI-powered ESG and carbon accounting "
        "compliance copilot."
    ),
    version="1.0.0",
)


# API routes
app.include_router(router)


# Frontend directory
frontend_path = Path("frontend")


# Serve CSS and JavaScript
app.mount(
    "/frontend",
    StaticFiles(directory=frontend_path),
    name="frontend",
)


# Dashboard
@app.get("/")
def root():

    return FileResponse(
        frontend_path / "index.html"
    )