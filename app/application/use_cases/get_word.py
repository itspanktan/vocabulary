"""Use case: fetch a single word by id."""
from __future__ import annotations

from app.application.unit_of_work import UnitOfWork
from app.domain.entities import Word
from app.domain.exceptions import WordNotFoundError


def get_word(uow: UnitOfWork, word_id: int) -> Word:
    with uow:
        word = uow.words.get(word_id)
        if word is None:
            raise WordNotFoundError(word_id)
        return word
