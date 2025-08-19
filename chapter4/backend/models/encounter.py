"""Pydantic models for encounters and monsters."""
from typing import List
from pydantic import BaseModel

class Monster(BaseModel):
    """A Pydantic model for a monster."""
    name: str
    challenge_rating: str
    description: str

class Encounter(BaseModel):
    """A Pydantic model for an encounter."""
    title: str
    description: str
    monsters: List[Monster]
    tactics: str
    terrain: str
