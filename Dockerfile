# pull official base image
FROM python:3.8.9-alpine3.13

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev curl openssl-dev cargo \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false 

# copy pyproject file
COPY ./pyproject.toml /usr/src/app/pyproject.toml

RUN poetry install

# copy project
COPY ./src /usr/src/app/
