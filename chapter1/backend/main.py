"""Main application file for the TTRPG GM Assistant API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.endpoints import router as api_router

app = FastAPI(
    title="TTRPG GM Assistant API",
    description="Backend API for the Streamlit GM Assistant.",
    version="0.1.0",
)

origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
