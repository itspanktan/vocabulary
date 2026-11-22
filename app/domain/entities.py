"""Domain entities.

An Entity is defined by its identity (``id``), not by its attribute values:
two Word entities with the same id are the same Word even if their
attributes have since diverged. This is why equality/hash are defined
manually below (``eq=False`` stops the dataclass from generating the usual
field-by-field comparison).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.value_objects import Definition, PartOfSpeech


@dataclass(eq=False)
class Word:
    id: int | None
    text: str
    part_of_speech: PartOfSpeech
    definitions: list[Definition] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return NotImplemented
        # Unsaved entities (id is None) have no identity yet, so two of them
        # are never considered the same Word even with identical attributes.
        return self.id is not None and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def add_definition(self, definition: Definition) -> None:
        if definition in self.definitions:
            raise ValueError(f"Duplicate definition for word '{self.text}'")
        self.definitions.append(definition)
