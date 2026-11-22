"""Unit tests for the Definition value object -- value-based equality and
immutability.
"""
import pytest

from app.domain.value_objects import Definition


def test_definitions_with_same_values_are_equal():
    a = Definition(text="to move fast", example_sentence="She ran to the store.")
    b = Definition(text="to move fast", example_sentence="She ran to the store.")

    assert a == b


def test_definitions_with_different_values_are_not_equal():
    a = Definition(text="to move fast")
    b = Definition(text="to move slowly")

    assert a != b


def test_definition_is_immutable():
    definition = Definition(text="to move fast")

    with pytest.raises(AttributeError):
        definition.text = "changed"


def test_definition_rejects_empty_text():
    with pytest.raises(ValueError):
        Definition(text="   ")
