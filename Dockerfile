ARG DOCKER_HOST=docker.io/library
ARG BUILD_ENV=dev

FROM $DOCKER_HOST/python:3.9-slim as base
WORKDIR /app

COPY requirements.txt requirements.txt

# Dev docker image template
FROM base as dev-img
RUN pip3 install -r requirements.txt

# Add docker image template here
# name template <name>-img (e.g. ci-img or test-img)

FROM ${BUILD_ENV}-img as prod-img

COPY app app
COPY alembic alembic
COPY alembic.ini .
COPY entrypoint.sh entrypoint.sh

EXPOSE 8080/udp
EXPOSE 8080/tcp

ENTRYPOINT ["sh","entrypoint.sh"]
