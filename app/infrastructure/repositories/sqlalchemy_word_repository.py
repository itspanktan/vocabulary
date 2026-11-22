"""SQLAlchemy implementation of ``WordRepository``.

Translates between the domain's ``Word`` entity / ``Definition`` value
objects and the ORM's ``WordModel`` / ``DefinitionModel`` rows.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities import Word
from app.domain.repositories import WordRepository
from app.domain.value_objects import Definition
from app.infrastructure.database.models import DefinitionModel, WordModel


class SqlAlchemyWordRepository(WordRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, word: Word) -> Word:
        model = WordModel(
            text=word.text,
            part_of_speech=word.part_of_speech,
            created_at=word.created_at,
            definitions=[
                DefinitionModel(text=d.text, example_sentence=d.example_sentence)
                for d in word.definitions
            ],
        )
        self._session.add(model)
        self._session.flush()  # assigns model.id without committing the transaction
        return self._to_entity(model)

    def get(self, word_id: int) -> Word | None:
        model = self._session.get(WordModel, word_id)
        return self._to_entity(model) if model else None

    def get_by_text(self, text: str) -> Word | None:
        model = self._session.scalar(select(WordModel).where(WordModel.text == text))
        return self._to_entity(model) if model else None

    def list(self) -> list[Word]:
        models = self._session.scalars(select(WordModel)).all()
        return [self._to_entity(m) for m in models]

    def delete(self, word_id: int) -> None:
        model = self._session.get(WordModel, word_id)
        if model is not None:
            self._session.delete(model)

    @staticmethod
    def _to_entity(model: WordModel) -> Word:
        return Word(
            id=model.id,
            text=model.text,
            part_of_speech=model.part_of_speech,
            definitions=[Definition(d.text, d.example_sentence) for d in model.definitions],
            created_at=model.created_at,
        )
