"""Main application file for the TTRPG GM Assistant API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

from backend.api.endpoints import router as api_router
from backend.database.database import create_db_and_tables

app = FastAPI(
    title="TTRPG GM Assistant API",
    description="Backend API for the Streamlit GM Assistant.",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    """Creates the database and tables on startup."""
    create_db_and_tables()


# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Create and mount the MCP server
mcp = FastApiMCP(app)
mcp.mount_http()
