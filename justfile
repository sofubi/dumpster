_default:
  just -l

format:
  uv run ruff format

lint:
  uv run ruff check ./src

pre-commit: format lint

test +ARGS='':
  uv run pytest {{ARGS}}

unit_test +ARGS='':
  uv run pytest {{ARGS}} --ignore=tests/integration

integration_test +ARGS='':
  uv run pytest {{ARGS}} --ignore=tests/unit

run +ARGS='':
  uv run dumpster {{ARGS}}
