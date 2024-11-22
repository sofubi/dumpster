# https://github.com/bmaingret/coach-planner/blob/main/docker/Dockerfile
# https://dteslya.engineer/blog/2022/07/14/how-to-run-a-python-cli-tool-inside-a-docker-container/#building-a-docker-image
# syntax=docker/dockerfile:1

ARG APP_NAME=dumpster
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.10
ARG UV_VERSION=0.5.2

#
# Stage: staging
#
FROM python:${PYTHON_VERSION}-slim as staging
ARG APP_NAME
ARG APP_PATH
ARG UV_VERSION

ENV \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONFAULTHANDLER=1

# Install UV
COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION}} /uv /uvx /bin/

# Import project files
WORKDIR ${APP_PATH}
ADD ./uv.lock ./pyproject.toml ./
ADD ./src ./src

# Mkdir for dump storage
RUN mkdir -p /data

#
# Stage: build
#
FROM staging as build
ARG APP_PATH

WORKDIR ${APP_PATH}
RUN uv build
RUN uv export --format requirements-txt --no-dev --no-hashes -o constraints.txt

#
# Stage: production
#
FROM python:${PYTHON_VERSION}-slim as production
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
COPY --from=build ${APP_PATH}/constraints.txt ./
RUN pip install ./${APP_NAME}*.whl --constraint constraints.txt

COPY ./docker/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# vim: filetype=dockerfile
