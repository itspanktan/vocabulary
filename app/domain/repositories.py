"""Abstract persistence contracts for the domain (the Repository pattern).

Concrete implementations live in ``app.infrastructure.repositories``.
Application and API code depend only on these interfaces, never on a
specific storage technology.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities import Word


class WordRepository(ABC):
    @abstractmethod
    def add(self, word: Word) -> Word:
        """Persist a new word and return it with its assigned id."""

    @abstractmethod
    def get(self, word_id: int) -> Word | None:
        """Return the word with the given id, or None if it doesn't exist."""

    @abstractmethod
    def get_by_text(self, text: str) -> Word | None:
        """Return the word matching the given text, or None."""

    @abstractmethod
    def list(self) -> list[Word]:
        """Return all words."""

    @abstractmethod
    def delete(self, word_id: int) -> None:
        """Remove the word with the given id."""
