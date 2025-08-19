"""This module contains the logic for generating combat encounters."""
import json
from typing import Dict, Any

from backend.prompts import ENCOUNTER_PROMPT_TEMPLATE
from backend.services.llm import client, json_generation_config, CHAT_MODEL


def generate_encounter_details(prompt: str) -> Dict[str, Any]:
    """
    Generates structured encounter details based on a prompt using a JSON-configured LLM.

    Args:
        prompt: The user's prompt describing the desired encounter.

    Returns:
        A dictionary containing the structured details of the generated encounter.
    """
    # 1. Format the prompt
    full_prompt = ENCOUNTER_PROMPT_TEMPLATE.format(prompt=prompt)

    # 2. Generate the content
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=full_prompt,
        config=json_generation_config,
    )

    # 3. Clean and parse the JSON response
    try:
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing JSON from LLM response: {e}")
        return {"error": "Failed to generate encounter details due to a JSON parsing error."}
