# Copied with minor modifications from wx-files-service

FROM ubuntu:24.04

LABEL maintainer="Lee Zeman <lzeman@uvic.ca>"

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -yq install \
        curl \
        libpq-dev \
        python3 \
        python3-dev \
        pipx \
        python3-pip \
        postgresql-client

ADD . /app
WORKDIR /app

RUN pipx install poetry
ENV PATH=/root/.local/bin:$PATH
RUN poetry install

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/readyz || exit 1

ENV FLASK_APP=hms.asgi
ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["poetry", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0", "--workers", "4", "hms.asgi:connexion_app"]
