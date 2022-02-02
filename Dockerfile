FROM python:3.9-slim

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
    # && apt purge -y netcat gcc python3-dev \
    # && apt clean -y && apt autoremove -y \

COPY . ./

CMD poetry run uvicorn --host=0.0.0.0 app.main:app