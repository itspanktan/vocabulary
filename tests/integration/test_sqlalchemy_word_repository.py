"""Integration tests for SqlAlchemyWordRepository.

Runs against an in-memory SQLite database rather than MySQL so these tests
are fast and need no external service. The ORM mapping is exactly the same
either way; only the connection string changes between here and production
(see app.config.Settings.database_url).
"""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities import Word
from app.domain.value_objects import Definition, PartOfSpeech
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import WordModel  # noqa: F401 registers the mapping
from app.infrastructure.repositories.sqlalchemy_word_repository import SqlAlchemyWordRepository


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db_session = factory()
    yield db_session
    db_session.close()


def test_add_and_get_round_trips_a_word(session):
    repo = SqlAlchemyWordRepository(session)
    word = Word(
        id=None,
        text="lucid",
        part_of_speech=PartOfSpeech.ADJECTIVE,
        definitions=[Definition(text="clear and easy to understand")],
    )

    saved = repo.add(word)
    session.commit()

    fetched = repo.get(saved.id)
    assert fetched.text == "lucid"
    assert fetched.definitions == [Definition(text="clear and easy to understand")]


def test_get_by_text_finds_existing_word(session):
    repo = SqlAlchemyWordRepository(session)
    repo.add(Word(id=None, text="terse", part_of_speech=PartOfSpeech.ADJECTIVE))
    session.commit()

    found = repo.get_by_text("terse")

    assert found is not None
    assert found.text == "terse"


def test_delete_removes_the_word(session):
    repo = SqlAlchemyWordRepository(session)
    saved = repo.add(Word(id=None, text="obsolete", part_of_speech=PartOfSpeech.ADJECTIVE))
    session.commit()

    repo.delete(saved.id)
    session.commit()

    assert repo.get(saved.id) is None
