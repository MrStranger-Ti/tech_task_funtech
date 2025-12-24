FROM python:3.12.11-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/usr/src/

WORKDIR usr/src

RUN pip install uv

COPY pyproject.toml ./pyproject.toml

COPY uv.lock ./uv.lock

RUN uv pip install --system -r pyproject.toml

COPY app ./app

COPY .env ./.env

COPY alembic.ini ./alembic.ini
