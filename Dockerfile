FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY tests ./tests

# Editable install so the ./app bind mount in docker-compose.yml (live code
# changes) is picked up without rebuilding the image.
RUN pip install --no-cache-dir -e '.[dev]'

EXPOSE 8000

CMD ["sh", "-c", "python -m app.infrastructure.bootstrap && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
