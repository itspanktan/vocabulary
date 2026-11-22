"""Use case: register a new word in the vocabulary."""
from __future__ import annotations

from app.application.unit_of_work import UnitOfWork
from app.domain.entities import Word
from app.domain.exceptions import DuplicateWordError
from app.domain.value_objects import Definition, PartOfSpeech


def create_word(
    uow: UnitOfWork,
    text: str,
    part_of_speech: PartOfSpeech,
    definitions: list[Definition],
) -> Word:
    with uow:
        if uow.words.get_by_text(text) is not None:
            raise DuplicateWordError(text)

        word = Word(id=None, text=text, part_of_speech=part_of_speech, definitions=list(definitions))
        saved = uow.words.add(word)
        uow.commit()
        return saved
