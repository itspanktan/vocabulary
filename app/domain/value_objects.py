"""Value objects: immutable, identity-less building blocks of the domain.

Two value objects are equal when their attributes are equal -- there is no
identity to compare, and once constructed they cannot change.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PartOfSpeech(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"


@dataclass(frozen=True)
class Definition:
    text: str
    example_sentence: str | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Definition text must not be empty")
