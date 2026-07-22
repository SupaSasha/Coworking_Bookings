FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"