"""Pydantic model for a Non-Player Character (NPC)."""
from typing import Literal
from pydantic import BaseModel

class NPC(BaseModel):
    """A Pydantic model for a Non-Player Character (NPC)."""
    name: str
    race: str
    vocation: str
    personality: str
    backstory: str
    motivations: str
    role_in_story: Literal["ally", "enemy", "quest giver", "neutral party", "red herring"]
