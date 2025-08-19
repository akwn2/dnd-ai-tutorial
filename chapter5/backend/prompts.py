"""This module contains all the prompt templates for the application."""

# --- NPC Generation ---
NPC_PROMPT_TEMPLATE = """
Based on the following prompt, generate a detailed Non-Player Character (NPC).
The JSON object should have the following keys: "name", "race", "vocation", "personality", "backstory", "motivations", and "role_in_story".

Prompt: {prompt}
"""

# --- Encounter Generation ---
ENCOUNTER_PROMPT_TEMPLATE = """
Based on the following prompt, generate a detailed combat encounter.
The JSON object should have the following keys: "title", "description", "monsters", "tactics", and "terrain".
The "monsters" key should be a list of objects, where each object has "name", "challenge_rating", and "description".

Prompt: {prompt}
"""

# --- RAG ---
RAG_PROMPT_TEMPLATE = """
Based on the following context from the campaign's lore documents, please answer the user's question.
If the context does not contain the answer, state that you don't have that information.

Context:
{context}

Question: {prompt}
"""
