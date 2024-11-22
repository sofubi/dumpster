# https://github.com/bmaingret/coach-planner/blob/main/docker/Dockerfile
# https://dteslya.engineer/blog/2022/07/14/how-to-run-a-python-cli-tool-inside-a-docker-container/#building-a-docker-image
# syntax=docker/dockerfile:1

ARG APP_NAME=dumpster
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.10
ARG UV_VERSION=0.5.4

#
# Stage: staging
#
FROM python:${PYTHON_VERSION}-slim AS staging
ARG APP_NAME
ARG APP_PATH
ARG UV_VERSION

ENV \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONFAULTHANDLER=1

# Install UV
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/

# Import project files
WORKDIR ${APP_PATH}
COPY --from=dumpster ./uv.lock ./pyproject.toml ./README.md ./.python-version ./
COPY --from=dumpster ./src ./src

# Mkdir for dump storage
RUN mkdir -p /data

#
# Stage: build
#
FROM staging AS build
ARG APP_PATH

WORKDIR ${APP_PATH}
RUN uv build

#
# Stage: production
#
FROM python:${PYTHON_VERSION}-slim AS production
ARG APP_NAME
ARG APP_PATH

ENV \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONFAULTHANDLER=1

ENV \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100

# Get wheel and instal against deps
WORKDIR ${APP_PATH}
COPY --from=build ${APP_PATH}/dist/*.whl ./
RUN pip install ./${APP_NAME}*.whl

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# vim: filetype=dockerfile
