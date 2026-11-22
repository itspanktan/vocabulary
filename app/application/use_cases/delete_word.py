"""Use case: remove a word from the vocabulary."""
from __future__ import annotations

from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import WordNotFoundError


def delete_word(uow: UnitOfWork, word_id: int) -> None:
    with uow:
        if uow.words.get(word_id) is None:
            raise WordNotFoundError(word_id)
        uow.words.delete(word_id)
        uow.commit()
