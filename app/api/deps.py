"""FastAPI dependency providers."""
from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session, sessionmaker

from app.application.unit_of_work import UnitOfWork
from app.config import settings
from app.infrastructure.database.session import create_db_engine, create_session_factory
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

engine = create_db_engine(settings)
_session_factory: sessionmaker[Session] = create_session_factory(engine)


def get_unit_of_work() -> Iterator[UnitOfWork]:
    yield SqlAlchemyUnitOfWork(_session_factory)
