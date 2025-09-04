"""This module centralizes the configuration and instantiation of the Google GenAI client."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Use GOOGLE_API_KEY from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# --- Client Instantiation ---
# The client is the central object for all interactions with the Gemini API.
client = genai.Client(api_key=api_key)

# Default model for chat/tool use
CHAT_MODEL = "gemini-2.5-flash"

# --- Reusable Generation Configs ---

# A config specifically for forcing JSON output for structured data generation
json_generation_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)
