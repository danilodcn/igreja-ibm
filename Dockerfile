FROM python:3.11-slim-buster


ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt update && \
    apt install libpq-dev libcurl4-openssl-dev libssl-dev default-libmysqlclient-dev gcc make libjpeg-dev curl git -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install poetry

WORKDIR /app

EXPOSE 8080
COPY pyproject.toml poetry.lock /app/

RUN poetry install --only main --no-root

COPY . .

CMD ["/usr/bin/make", "run"]
