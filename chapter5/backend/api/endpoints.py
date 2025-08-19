"""API endpoints for the TTRPG GM Assistant."""
import asyncio
import json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Iterable, Any
from google.genai import types

from backend.database.database import add_message_to_db, get_messages_from_db
from backend.rag.rag import ask_rag_question
from backend.services.dice_roller import roll_dice_sync
from backend.services.encounter_generator import generate_encounter_details
from backend.services.llm import client, CHAT_MODEL
from backend.services.npc_generator import generate_npc_details

router = APIRouter()

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    prompt: str
    thread_id: str

class ToolRequest(BaseModel):
    prompt: str

# --- Helper Functions ---
def parts_to_dict(parts: Iterable[Any]) -> list[dict]:
    """Converts a list of Gemini Parts to a JSON-serializable list of dictionaries."""
    serializable_parts = []
    for part in parts:
        part_dict = {}
        if hasattr(part, "text") and part.text:
            part_dict["text"] = part.text
        if (fc := getattr(part, "function_call", None)):
            part_dict["functionCall"] = {
                "name": fc.name,
                "args": dict(fc.args),
            }
        if (fr := getattr(part, "function_response", None)):
            part_dict["functionResponse"] = {
                "name": fr.name,
                "response": dict(fr.response),
            }
        if part_dict:
            serializable_parts.append(part_dict)
    return serializable_parts


def normalize_tool_output(output: Any) -> dict:
    """Ensures tool outputs are dicts as required by FunctionResponse."""
    if isinstance(output, dict):
        return output
    return {"output": output}


def filter_history_for_api(messages: list[dict]) -> list[dict]:
    """Filters persisted messages to only API-acceptable parts (text, functionResponse)."""
    safe_history: list[dict] = []
    for msg in messages:
        role = msg.get("role")
        safe_parts: list[dict] = []
        for part in msg.get("parts", []):
            if "text" in part:
                safe_parts.append({"text": part["text"]})
            elif "functionResponse" in part:
                # pass-through (already serializable)
                safe_parts.append(part)
            # intentionally skip functionCall objects
        if safe_parts:
            safe_history.append({"role": role, "parts": safe_parts})
    return safe_history

# --- Agent and Tool Definitions ---
# See: https://ai.google.dev/gemini-api/docs/function-calling
tools = types.Tool(
    function_declarations=[
        {
            "name": "generate_npc",
            "description": "Generates a non-player character (NPC). Input should be a descriptive prompt.",
            "parameters": {
                "type": "object",
                "properties": {"prompt": {"type": "string"}},
                "required": ["prompt"],
            },
        },
        {
            "name": "generate_encounter",
            "description": "Generates a combat encounter. Input should be a descriptive prompt.",
            "parameters": {
                "type": "object",
                "properties": {"prompt": {"type": "string"}},
                "required": ["prompt"],
            },
        },
        {
            "name": "roll_dice",
            "description": "Rolls dice. Input should be a standard dice notation string (e.g., '2d6', '1d20+5').",
            "parameters": {
                "type": "object",
                "properties": {"dice_string": {"type": "string"}},
                "required": ["dice_string"],
            },
        },
        {
            "name": "ask_lore_keeper",
            "description": "Answers questions about campaign lore. Input should be the user's question.",
            "parameters": {
                "type": "object",
                "properties": {"prompt": {"type": "string"}},
                "required": ["prompt"],
            },
        },
    ]
)

tool_functions = {
    "generate_npc": generate_npc_details,
    "generate_encounter": generate_encounter_details,
    "roll_dice": roll_dice_sync,
    "ask_lore_keeper": ask_rag_question,
}

# --- API Endpoints ---
@router.post("/chat")
async def chat(request: ChatRequest):
    """The main agent endpoint with a multi-step reasoning loop."""
    # We will use the shared client and specify tools in the config

    # Start from persisted history, but only keep API-acceptable parts
    history = filter_history_for_api(get_messages_from_db(request.thread_id))
    user_message = {"role": "user", "parts": [{"text": request.prompt}]}
    add_message_to_db(request.thread_id, user_message)
    history.append(user_message)

    # --- Core Agent Loop ---
    # This loop allows the model to make multiple tool calls to fulfill a request.
    # See: https://ai.google.dev/gemini-api/docs/thinking
    while True:
        response = client.models.generate_content(
            model=CHAT_MODEL,
            contents=history,
            config=types.GenerateContentConfig(tools=[tools]),
        )

        parts = []
        if getattr(response, "candidates", None):
            candidate = response.candidates[0]
            if getattr(candidate, "content", None):
                parts = list(getattr(candidate.content, "parts", []) or [])

        # Check if the model's response contains any tool calls
        function_calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
        if not function_calls:
            # No tool call, this is the final answer
            serializable_parts = parts_to_dict(parts)
            add_message_to_db(request.thread_id, {"role": "model", "parts": serializable_parts})
            break

        # --- Process Tool Calls ---
        # Save the model's tool-calling response to the database (for UI only)
        serializable_parts = parts_to_dict(parts)
        add_message_to_db(request.thread_id, {"role": "model", "parts": serializable_parts})

        # IMPORTANT: Do NOT append model functionCall parts to API history

        # 3. Execute the function calls and gather responses
        tool_response_parts = []
        for fc in function_calls:
            function_name = fc.name
            function_args = dict(fc.args)

            if function_name in tool_functions:
                function_to_call = tool_functions[function_name]

                # Await coroutines, run sync functions in a thread
                if asyncio.iscoroutinefunction(function_to_call):
                    tool_output = await function_to_call(**function_args)
                else:
                    tool_output = await asyncio.to_thread(function_to_call, **function_args)

                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=function_name,
                        response=normalize_tool_output(tool_output),
                    )
                )

        # 4. Add tool responses to history and continue the loop
        if tool_response_parts:
            # Add serializable version to the database
            serializable_tool_responses = parts_to_dict(tool_response_parts)
            add_message_to_db(request.thread_id, {"role": "user", "parts": serializable_tool_responses})

            # Add rich object version to in-memory history
            history.append({"role": "user", "parts": tool_response_parts})

    return {"status": "ok"}


@router.post("/generate_npc")
async def generate_npc_endpoint(request: ToolRequest):
    """Generates a non-player character (NPC)."""
    return await asyncio.to_thread(generate_npc_details, request.prompt)


@router.post("/generate_encounter")
async def generate_encounter_endpoint(request: ToolRequest):
    """Generates a combat encounter."""
    return await asyncio.to_thread(generate_encounter_details, request.prompt)


@router.post("/roll_dice")
async def roll_dice_endpoint(request: ToolRequest):
    """Rolls dice based on a standard dice notation string."""
    return await asyncio.to_thread(roll_dice_sync, request.prompt)


@router.post("/ask_lore_keeper")
async def ask_lore_keeper_endpoint(request: ToolRequest):
    """Answers questions about the campaign's lore and world."""
    return await asyncio.to_thread(ask_rag_question, request.prompt)


@router.get("/")
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "TTRPG GM Assistant API is running!"}


@router.get("/history/{thread_id}")
async def get_history(thread_id: str):
    """Retrieves the chat history for a given thread_id."""
    messages = get_messages_from_db(thread_id)
    return {"messages": messages}
