FROM python:3.10.2-alpine as requirements-stage

WORKDIR /tmp
RUN apk update && apk upgrade
RUN apk add --no-cache bash\
                       python2 \
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       python2-dev \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install setuptools==30.1.0

RUN  pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.2-alpine

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
