"""Domain-level exceptions.

Raised by domain/application code and translated into HTTP responses at the
API boundary (see app.api.routers).
"""
from __future__ import annotations


class WordNotFoundError(Exception):
    def __init__(self, word_id: int) -> None:
        super().__init__(f"Word with id {word_id} was not found")
        self.word_id = word_id


class DuplicateWordError(Exception):
    def __init__(self, text: str) -> None:
        super().__init__(f"Word '{text}' already exists")
        self.text = text
