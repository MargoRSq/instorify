# no matter which version you choose 3.9.x -> always will be 3.9,2
FROM python:3.9.2-slim

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
