"""
CarbonTrace AI
FastAPI Application
"""

from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI

from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from backend.api.routes import router


# -------------------------------------------------
# Load environment variables
# -------------------------------------------------

load_dotenv()


# -------------------------------------------------
# Project paths
# -------------------------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

FRONTEND_DIR = (
    BASE_DIR / "frontend"
)


# -------------------------------------------------
# FastAPI application
# -------------------------------------------------

app = FastAPI(

    title="CarbonTrace AI",

    description=(
        "AI-powered ESG and carbon accounting "
        "compliance copilot."
    ),

    version="1.0.0",
)


# -------------------------------------------------
# API routes
# -------------------------------------------------

app.include_router(
    router
)


# -------------------------------------------------
# Serve frontend
# -------------------------------------------------

app.mount(

    "/frontend",

    StaticFiles(
        directory=FRONTEND_DIR
    ),

    name="frontend",
)


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@app.get("/")
def root():

    return FileResponse(

        FRONTEND_DIR /
        "index.html"

    )