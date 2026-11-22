"""Unit tests for the get_word use case."""
import pytest

from app.application.use_cases.create_word import create_word
from app.application.use_cases.get_word import get_word
from app.domain.exceptions import WordNotFoundError
from app.domain.value_objects import PartOfSpeech
from tests.fakes import FakeUnitOfWork


def test_get_word_returns_existing_word():
    uow = FakeUnitOfWork()
    created = create_word(uow, text="lucid", part_of_speech=PartOfSpeech.ADJECTIVE, definitions=[])

    found = get_word(uow, created.id)

    assert found == created


def test_get_word_raises_when_missing():
    uow = FakeUnitOfWork()

    with pytest.raises(WordNotFoundError):
        get_word(uow, 999)
