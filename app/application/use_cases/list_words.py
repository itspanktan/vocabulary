"""Use case: list every word in the vocabulary."""
from __future__ import annotations

from app.application.unit_of_work import UnitOfWork
from app.domain.entities import Word


def list_words(uow: UnitOfWork) -> list[Word]:
    with uow:
        return uow.words.list()
