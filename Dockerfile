# ---------- Base ----------
FROM python:3.14.6-slim AS base

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./


# ---------- Development ----------
FROM base AS development

RUN uv sync --locked

COPY app ./app
COPY tests ./tests
COPY alembic.ini ./
COPY alembic ./alembic

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ---------- Builder ----------
FROM base AS builder

RUN uv sync --locked --no-dev


# ---------- Runtime ----------
FROM python:3.14.6-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]