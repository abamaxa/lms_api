import logging

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_summarizer_service
from app.routers import summarizer

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load the model on startup
    get_summarizer_service()
    yield


app = FastAPI(
    title="Text Summarizer API",
    description="A RESTful API for text summarization",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarizer.router, prefix="/api/v1", tags=["summarizer"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Text Summarizer API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
