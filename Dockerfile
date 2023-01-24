
FROM python:3.10.2-alpine3.14 as requirements-stage

WORKDIR /tmp

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.2-alpine3.14


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat gcc python3-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
COPY .env ./

RUN pip install poetry==1.1 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

COPY . ./

CMD poetry run uvicorn --host=0.0.0.0 app.main:app
