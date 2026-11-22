"""Unit of Work: groups repository operations into one atomic transaction.

Exiting the ``with`` block rolls back by default -- a use case must call
``commit()`` explicitly to persist its changes. That makes "forgot to
commit" fail safe instead of silently succeeding.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.repositories import WordRepository


class UnitOfWork(ABC):
    words: WordRepository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, *args: object) -> None:
        self.rollback()

    def commit(self) -> None:
        self._commit()

    @abstractmethod
    def _commit(self) -> None:
        """Persist all changes made during this unit of work."""

    @abstractmethod
    def rollback(self) -> None:
        """Discard all changes made during this unit of work."""
