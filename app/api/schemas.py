"""Pydantic DTOs for the HTTP API.

Kept separate from domain entities/value objects so the API's wire format
can evolve independently of the domain model.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.value_objects import PartOfSpeech


class DefinitionSchema(BaseModel):
    model_config = {"from_attributes": True}

    text: str
    example_sentence: str | None = None


class WordCreateSchema(BaseModel):
    text: str = Field(min_length=1, max_length=100)
    part_of_speech: PartOfSpeech
    definitions: list[DefinitionSchema] = Field(default_factory=list)


class WordReadSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    text: str
    part_of_speech: PartOfSpeech
    definitions: list[DefinitionSchema]
    created_at: datetime
