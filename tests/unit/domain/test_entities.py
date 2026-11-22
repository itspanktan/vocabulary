"""Unit tests for the Word entity -- identity-based equality."""
import pytest

from app.domain.entities import Word
from app.domain.value_objects import Definition, PartOfSpeech


def test_words_with_same_id_are_equal_even_if_attributes_differ():
    a = Word(id=1, text="serendipity", part_of_speech=PartOfSpeech.NOUN)
    b = Word(id=1, text="different text", part_of_speech=PartOfSpeech.VERB)

    assert a == b


def test_unsaved_words_are_never_equal():
    a = Word(id=None, text="serendipity", part_of_speech=PartOfSpeech.NOUN)
    b = Word(id=None, text="serendipity", part_of_speech=PartOfSpeech.NOUN)

    assert a != b


def test_words_with_different_ids_are_not_equal():
    a = Word(id=1, text="serendipity", part_of_speech=PartOfSpeech.NOUN)
    b = Word(id=2, text="serendipity", part_of_speech=PartOfSpeech.NOUN)

    assert a != b


def test_add_definition_rejects_duplicates():
    word = Word(id=1, text="run", part_of_speech=PartOfSpeech.VERB)
    definition = Definition(text="to move fast")
    word.add_definition(definition)

    with pytest.raises(ValueError):
        word.add_definition(definition)
