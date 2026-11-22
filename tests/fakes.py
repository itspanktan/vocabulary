"""In-memory fakes so use cases and API routes can be unit tested without a
real database.
"""
from __future__ import annotations

from app.application.unit_of_work import UnitOfWork
from app.domain.entities import Word
from app.domain.repositories import WordRepository


class FakeWordRepository(WordRepository):
    def __init__(self) -> None:
        self._words: dict[int, Word] = {}
        self._next_id = 1

    def add(self, word: Word) -> Word:
        word.id = self._next_id
        self._words[word.id] = word
        self._next_id += 1
        return word

    def get(self, word_id: int) -> Word | None:
        return self._words.get(word_id)

    def get_by_text(self, text: str) -> Word | None:
        return next((w for w in self._words.values() if w.text == text), None)

    def list(self) -> list[Word]:
        return list(self._words.values())

    def delete(self, word_id: int) -> None:
        self._words.pop(word_id, None)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.words = FakeWordRepository()
        self.committed = False

    def _commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass
