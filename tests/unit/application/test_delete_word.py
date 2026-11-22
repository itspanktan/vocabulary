"""Unit tests for the delete_word use case."""
import pytest

from app.application.use_cases.create_word import create_word
from app.application.use_cases.delete_word import delete_word
from app.application.use_cases.get_word import get_word
from app.domain.exceptions import WordNotFoundError
from app.domain.value_objects import PartOfSpeech
from tests.fakes import FakeUnitOfWork


def test_delete_word_removes_it():
    uow = FakeUnitOfWork()
    word = create_word(uow, text="obsolete", part_of_speech=PartOfSpeech.ADJECTIVE, definitions=[])

    delete_word(uow, word.id)

    with pytest.raises(WordNotFoundError):
        get_word(uow, word.id)


def test_delete_word_raises_when_missing():
    uow = FakeUnitOfWork()

    with pytest.raises(WordNotFoundError):
        delete_word(uow, 999)
