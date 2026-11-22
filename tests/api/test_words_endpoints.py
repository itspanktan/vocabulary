"""API tests -- exercise the HTTP layer through FastAPI's TestClient, with
the Unit of Work dependency overridden to a fake so no real database is
needed.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_unit_of_work
from app.main import app
from tests.fakes import FakeUnitOfWork


@pytest.fixture()
def client():
    fake_uow = FakeUnitOfWork()
    app.dependency_overrides[get_unit_of_work] = lambda: fake_uow
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_then_get_word(client):
    response = client.post(
        "/words",
        json={
            "text": "lucid",
            "part_of_speech": "adjective",
            "definitions": [{"text": "clear and easy to understand"}],
        },
    )
    assert response.status_code == 201
    word_id = response.json()["id"]

    get_response = client.get(f"/words/{word_id}")
    assert get_response.status_code == 200
    assert get_response.json()["text"] == "lucid"


def test_create_duplicate_word_returns_409(client):
    payload = {"text": "terse", "part_of_speech": "adjective", "definitions": []}
    client.post("/words", json=payload)

    response = client.post("/words", json=payload)

    assert response.status_code == 409


def test_get_missing_word_returns_404(client):
    response = client.get("/words/999")

    assert response.status_code == 404


def test_list_words_returns_created_words(client):
    client.post("/words", json={"text": "terse", "part_of_speech": "adjective", "definitions": []})

    response = client.get("/words")

    assert response.status_code == 200
    assert any(w["text"] == "terse" for w in response.json())


def test_delete_word(client):
    create_response = client.post(
        "/words", json={"text": "obsolete", "part_of_speech": "adjective", "definitions": []}
    )
    word_id = create_response.json()["id"]

    delete_response = client.delete(f"/words/{word_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/words/{word_id}")
    assert get_response.status_code == 404
