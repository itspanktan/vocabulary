"""Unit tests for the list_words use case."""
from app.application.use_cases.create_word import create_word
from app.application.use_cases.list_words import list_words
from app.domain.value_objects import PartOfSpeech
from tests.fakes import FakeUnitOfWork


def test_list_words_returns_all_created_words():
    uow = FakeUnitOfWork()
    create_word(uow, text="lucid", part_of_speech=PartOfSpeech.ADJECTIVE, definitions=[])
    create_word(uow, text="terse", part_of_speech=PartOfSpeech.ADJECTIVE, definitions=[])

    words = list_words(uow)

    assert {w.text for w in words} == {"lucid", "terse"}


def test_list_words_returns_empty_list_when_none_exist():
    uow = FakeUnitOfWork()

    assert list_words(uow) == []
