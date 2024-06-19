FROM python:3.12-slim

WORKDIR /app

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8 \
  PATH="${PATH}:/root/.poetry/bin" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app/snapp_mle_task \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  TZ=Asia/Tehran

RUN apt update && apt upgrade -y && apt install make curl gcc postgresql postgresql-contrib pkg-config libpq-dev -y && rm -rf /var/lib/apt/lists/* && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
  cd /usr/local/bin && \
  ln -s /opt/poetry/bin/poetry && \
  poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install -n --no-root

COPY . /app

CMD uvicorn snapp_mle_task.main:app --host 0.0.0.0 --port 80 --log-level ${LOG_LEVEL} --reload
