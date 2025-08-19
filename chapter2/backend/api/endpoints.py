"""API endpoints for the TTRPG GM Assistant."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.exceptions import OutputParserException
from backend.models.npc import NPC
from backend.services.npc_generator import npc_chain


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
    return {"response": f"The GM assistant received your prompt: '{prompt.prompt}'"}

@router.post("/generate_npc", response_model=NPC)
async def generate_npc(prompt: Prompt):
    """
    Endpoint to generate a new NPC based on a prompt.
    This now uses a LangChain to get a structured response from the LLM.
    """
    try:
        # Run the LangChain to generate the NPC
        npc_data = await npc_chain.ainvoke({"prompt": prompt.prompt})
        return npc_data
    except OutputParserException as e:
        print(f"OutputParserException: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM output: {e}") from e
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}") from e
