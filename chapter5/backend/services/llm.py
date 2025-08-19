"""This module centralizes the configuration and instantiation of the Google GenAI client."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# --- Centralized Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment. Please set it in your .env file.")

# --- Client Instantiation ---
# The client is the central object for all interactions with the Gemini API.
client = genai.Client(api_key=GOOGLE_API_KEY)

# Default model for chat/tool use
CHAT_MODEL = "gemini-2.5-flash"

# --- Reusable Generation Configs ---

# A config specifically for forcing JSON output for structured data generation
json_generation_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)
