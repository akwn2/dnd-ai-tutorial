"""This module contains the logic for generating NPCs."""
import json
from typing import Dict, Any

from backend.prompts import NPC_PROMPT_TEMPLATE
from backend.services.llm import client, json_generation_config, CHAT_MODEL


def generate_npc_details(prompt: str) -> Dict[str, Any]:
    """
    Generates structured NPC details based on a prompt using a JSON-configured LLM.

    Args:
        prompt: The user's prompt describing the desired NPC.

    Returns:
        A dictionary containing the structured details of the generated NPC.
    """
    # 1. Format the prompt using the template
    full_prompt = NPC_PROMPT_TEMPLATE.format(prompt=prompt)

    # 2. Generate the content using the JSON-configured model
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=full_prompt,
        config=json_generation_config,
    )

    # 3. Clean and parse the JSON response
    try:
        # The response text might be wrapped in markdown fences
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing JSON from LLM response: {e}")
        return {"error": "Failed to generate NPC details due to a JSON parsing error."}
