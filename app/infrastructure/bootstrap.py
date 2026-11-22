"""Dev-only schema bootstrap.

No migration tool (e.g. Alembic) exists yet. Run this once against a fresh
database so the tables exist before the API starts -- see the Dockerfile's
CMD. Replace with real migrations before this app has data worth preserving
across schema changes.
"""
from __future__ import annotations

import time

from sqlalchemy.exc import OperationalError

from app.api.deps import engine
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import WordModel  # noqa: F401 registers the mapping

_MAX_ATTEMPTS = 30
_RETRY_SECONDS = 2


def create_tables() -> None:
    # The MySQL container's own startup does an internal bootstrap-then-restart
    # cycle, which can briefly report healthy before the real server is up --
    # so retry here instead of relying solely on docker-compose's health gate.
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            Base.metadata.create_all(engine)
            return
        except OperationalError:
            if attempt == _MAX_ATTEMPTS:
                raise
            print(f"Database not ready yet (attempt {attempt}/{_MAX_ATTEMPTS}), retrying...")
            time.sleep(_RETRY_SECONDS)


if __name__ == "__main__":
    create_tables()
