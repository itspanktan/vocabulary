# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

English vocabulary app: FastAPI backend (Python, MySQL via SQLAlchemy) under `app/`, React frontend
under `frontend/`. The backend follows the layered DDD architecture below; the frontend is a thin Vite +
React client that calls the `/words` HTTP API.

## Environment

- Requires Python >= 3.14 (see `pyproject.toml`). A `.venv` virtualenv exists at the repo root.
- `uv` is available for dependency installs (`pip` is not present in the venv by default).
- Copy `.env.example` to `.env` and point `VOCAB_DB_*` at a real MySQL instance before running the app
  for real. Tests never touch MySQL (see Testing below).

## Commands

Backend, from the repo root:

```
uv pip install --python .venv/bin/python -e '.[dev]'   # install backend + test deps
.venv/bin/python -m uvicorn app.main:app --reload       # run the API
.venv/bin/python -m pytest                               # full suite
.venv/bin/python -m pytest tests/unit/domain/test_entities.py::test_unsaved_words_are_never_equal  # single test
```

Frontend, from `frontend/`:

```
npm install
npm run dev     # Vite dev server, proxies /api to the backend on :8000
npm run build
npm test        # vitest
```

Whole stack via Docker Compose (MySQL + backend + frontend, hot reload on both):

```
docker compose up --build
```

`./app`/`./tests` and `./frontend/src` are bind-mounted into their containers, so edits take effect
without a rebuild. There's no migration tool yet — `app/infrastructure/bootstrap.py` runs
`Base.metadata.create_all` before `uvicorn` starts (wired into the `Dockerfile`'s `CMD`); it's
intentionally not a FastAPI startup hook, since that would make every `TestClient`-based test try to
open a real MySQL connection.

## Testing

- `tests/unit/` — domain and application-layer tests. Application tests run against
  `tests/fakes.py` (`FakeWordRepository` / `FakeUnitOfWork`), an in-memory stand-in for the real
  repository/UoW — no database involved.
- `tests/integration/` — exercises `SqlAlchemyWordRepository` against an in-memory SQLite engine
  (same ORM mapping as production MySQL, different connection string) so these stay fast and need no
  external service.
- `tests/api/` — FastAPI `TestClient` tests with the `get_unit_of_work` dependency overridden to a fake,
  so the HTTP layer is tested without a live database.
- There are currently no tests that require a running MySQL instance. If you add one, gate it behind an
  env var or a marker so `pytest` still passes with no database available.

## Architecture standards

The backend is a layered, domain-driven system under `app/`. Apply these patterns to every new module —
do not let code grow organically without them.

- **Layering**: `app/domain/` (entities, value objects, domain exceptions, repository interfaces) →
  `app/application/` (use cases, the `UnitOfWork` abstraction) → `app/infrastructure/` (SQLAlchemy
  models, the concrete repository and Unit of Work, DB session setup) → `app/api/` (FastAPI routers,
  Pydantic DTOs, dependency wiring). Domain code must not import from application, infrastructure, or
  api. Each use case in `app/application/use_cases/` is a single function that opens one `UnitOfWork`,
  does its repository calls, and either raises a domain exception or commits — see
  `app/application/use_cases/create_word.py` for the canonical shape.
- **Entities vs Value Objects**: `app/domain/entities.py` (`Word`) has an identity (`id`) — equality is
  by id, defined manually with `@dataclass(eq=False)` plus hand-written `__eq__`/`__hash__` (letting the
  dataclass auto-generate `__eq__` here would do field-by-field comparison, which is wrong for an
  entity). `app/domain/value_objects.py` (`Definition`) is a `@dataclass(frozen=True)` — equality by
  attributes, immutable, validated in `__post_init__`. Model each new concept as whichever one it
  actually is.
- **Repository pattern**: `app/domain/repositories.py` defines the `WordRepository` interface;
  `app/infrastructure/repositories/sqlalchemy_word_repository.py` is the only concrete implementation,
  translating between `Word`/`Definition` and the `WordModel`/`DefinitionModel` ORM rows. Application
  and API code depend only on the `WordRepository` interface, never on SQLAlchemy directly. Tests get a
  third implementation, `FakeWordRepository` in `tests/fakes.py`, so use cases are testable without a
  database.
- **Unit of Work pattern**: `app/application/unit_of_work.py` defines the abstract `UnitOfWork`
  (`__enter__`/`__exit__` roll back by default; a use case must call `.commit()` explicitly, so a
  forgotten commit fails safe). `app/infrastructure/unit_of_work.py` (`SqlAlchemyUnitOfWork`) is the
  concrete, session-backed implementation; `tests/fakes.py` (`FakeUnitOfWork`) is the in-memory one. One
  Unit of Work per use case call — never share one across multiple logical operations.
- **Documentation**: every module, class, and non-trivial function should carry a docstring explaining
  its responsibility (not just restating its name) — see any file under `app/` for the expected style.
  Use inline comments for the *why* behind a design decision, a non-obvious invariant, or a tradeoff —
  not for narrating what the code visibly does. Record significant architectural decisions (choice of
  storage, boundaries between layers, pattern deviations) in an `ARCHITECTURE.md` (or a `docs/adr/`
  folder of short ADRs) so the reasoning survives beyond the code.
