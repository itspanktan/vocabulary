"""Unit tests for the create_word use case, against a fake repository."""
import pytest

from app.application.use_cases.create_word import create_word
from app.domain.exceptions import DuplicateWordError
from app.domain.value_objects import Definition, PartOfSpeech
from tests.fakes import FakeUnitOfWork


def test_create_word_persists_and_commits():
    uow = FakeUnitOfWork()

    word = create_word(
        uow,
        text="ephemeral",
        part_of_speech=PartOfSpeech.ADJECTIVE,
        definitions=[Definition(text="lasting a very short time")],
    )

    assert word.id is not None
    assert uow.words.get(word.id) == word
    assert uow.committed is True


def test_create_word_rejects_duplicate_text():
    uow = FakeUnitOfWork()
    create_word(uow, text="ephemeral", part_of_speech=PartOfSpeech.ADJECTIVE, definitions=[])

    with pytest.raises(DuplicateWordError):
        create_word(uow, text="ephemeral", part_of_speech=PartOfSpeech.NOUN, definitions=[])
