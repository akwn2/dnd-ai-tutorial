"""API endpoints for the TTRPG GM Assistant."""
from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from backend.models.chat import ChatRequest
from backend.database.database import get_messages_from_db, add_message_to_db
from backend.services.graph import graph

router = APIRouter()

@router.get("/")
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "TTRPG GM Assistant API is running!"}

@router.post("/chat")
async def chat(request: ChatRequest):
    """Handles a chat request, invokes the LangGraph, and saves the conversation."""
    history = get_messages_from_db(request.thread_id)
    input_message = HumanMessage(content=request.prompt)
    
    current_messages = history + [input_message]
    
    result = graph.invoke({"messages": current_messages})
    
    ai_response = result["messages"][-1]
    
    add_message_to_db(request.thread_id, input_message)
    add_message_to_db(request.thread_id, ai_response)
    
    return {"status": "ok"}

@router.get("/history/{thread_id}")
async def get_history(thread_id: str):
    """Retrieves the chat history for a given thread_id."""
    messages = get_messages_from_db(thread_id)
    return {"messages": [msg.dict() for msg in messages]}
