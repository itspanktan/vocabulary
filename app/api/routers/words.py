"""HTTP routes for word resources.

Thin adapters: they call application use cases and translate domain
exceptions into HTTP responses. No business logic lives here.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_unit_of_work
from app.api.schemas import WordCreateSchema, WordReadSchema
from app.application.unit_of_work import UnitOfWork
from app.application.use_cases.create_word import create_word
from app.application.use_cases.delete_word import delete_word
from app.application.use_cases.get_word import get_word
from app.application.use_cases.list_words import list_words
from app.domain.exceptions import DuplicateWordError, WordNotFoundError
from app.domain.value_objects import Definition

router = APIRouter(prefix="/words", tags=["words"])


@router.post("", response_model=WordReadSchema, status_code=status.HTTP_201_CREATED)
def create_word_endpoint(
    payload: WordCreateSchema, uow: UnitOfWork = Depends(get_unit_of_work)
) -> WordReadSchema:
    definitions = [Definition(d.text, d.example_sentence) for d in payload.definitions]
    try:
        word = create_word(uow, payload.text, payload.part_of_speech, definitions)
    except DuplicateWordError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return WordReadSchema.model_validate(word)


@router.get("/{word_id}", response_model=WordReadSchema)
def get_word_endpoint(word_id: int, uow: UnitOfWork = Depends(get_unit_of_work)) -> WordReadSchema:
    try:
        word = get_word(uow, word_id)
    except WordNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return WordReadSchema.model_validate(word)


@router.get("", response_model=list[WordReadSchema])
def list_words_endpoint(uow: UnitOfWork = Depends(get_unit_of_work)) -> list[WordReadSchema]:
    words = list_words(uow)
    return [WordReadSchema.model_validate(w) for w in words]


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word_endpoint(word_id: int, uow: UnitOfWork = Depends(get_unit_of_work)) -> None:
    try:
        delete_word(uow, word_id)
    except WordNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
