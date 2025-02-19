# Copied with minor modifications from wx-files-service

FROM ubuntu:22.04

MAINTAINER Lee Zeman <lzeman@uvic.ca>

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -yq install \
        libpq-dev \
        python3 \
        python3-dev \
        python3-pip \
        postgresql-client \
	wget

ADD . /app
WORKDIR /app

RUN wget -O - https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH
RUN poetry install

EXPOSE 8000

ENV FLASK_APP hms.asgi
ENV FLASK_ENV development
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD poetry run uvicorn --port 8000 --host 0.0.0.0 --reload hms.asgi:connexion_app