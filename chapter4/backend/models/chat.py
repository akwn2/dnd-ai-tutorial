"""Pydantic models for chat requests and LangGraph agent state."""
from typing import TypedDict, Annotated
from operator import add
from pydantic import BaseModel
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """A TypedDict for the LangGraph agent state."""
    messages: Annotated[list[BaseMessage], add]
    next_node: str

class ChatRequest(BaseModel):
    """A Pydantic model for a chat request."""
    thread_id: str
    prompt: str
