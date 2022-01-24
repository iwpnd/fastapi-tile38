# pull official base image
FROM python:3.9.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN set -eux \
    && apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install curl \
    && pip install --upgrade pip \
    && rm -rf /root/.cache/pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# copy pyproject file
COPY ./pyproject.toml /usr/src/app/pyproject.toml

RUN poetry install

# copy project
COPY ./src /usr/src/app/
