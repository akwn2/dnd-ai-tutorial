"""API endpoints for the TTRPG GM Assistant."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Prompt(BaseModel):
    """A Pydantic model for a simple text prompt."""
    prompt: str

@router.get("/")
async def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "TTRPG GM Assistant API is running!"}

@router.post("/generate_response")
async def generate_response(prompt: Prompt):
    """Generates a generic response for a given prompt."""
    # This is a general placeholder for other types of requests
    return {"response": f"The GM assistant received your prompt: '{prompt.prompt}'"}
