# Vocabulary

An English vocabulary app: FastAPI + MySQL backend, React frontend.

## Docker Compose

Runs MySQL, the backend (with hot reload), and the frontend dev server together:

```
docker compose up --build
```

- Backend: http://localhost:8000 (tables are auto-created on container start -- see
  `app/infrastructure/bootstrap.py`; there's no migration tool yet)
- Frontend: http://localhost:5173
- MySQL: localhost:3306 (root password defaults to `vocabulary`; override with a `MYSQL_ROOT_PASSWORD`
  env var or in `.env`)

`./app` and `./tests` are bind-mounted into the backend container, and `./frontend/src` into the
frontend container, so local edits take effect without rebuilding the image.

## Backend

```
pip install -e '.[dev]'
cp .env.example .env   # then point it at your MySQL instance
uvicorn app.main:app --reload
```

Run tests:

```
pytest
```

## Frontend

```
cd frontend
npm install
npm run dev
```

See `CLAUDE.md` for the backend's architecture (domain / application / infrastructure / api layers,
Repository and Unit of Work patterns).
