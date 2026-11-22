"""SQLAlchemy ORM models -- the persistence shape of the domain.

These are intentionally separate from the domain entities/value objects in
``app.domain``: ORM models describe table columns, while domain objects
describe behavior and invariants. Mapping between the two happens in the
repository layer (see ``app.infrastructure.repositories``).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects import PartOfSpeech
from app.infrastructure.database.base import Base


class WordModel(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    part_of_speech: Mapped[PartOfSpeech] = mapped_column(SAEnum(PartOfSpeech), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    definitions: Mapped[list["DefinitionModel"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )


class DefinitionModel(Base):
    __tablename__ = "definitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    example_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)

    word: Mapped["WordModel"] = relationship(back_populates="definitions")
