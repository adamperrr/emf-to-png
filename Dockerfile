FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends inkscape curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi

COPY app.py .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
