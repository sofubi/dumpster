_default:
  just -l

format:
  uv run black ./src

lint:
  uv run ruff check --fix ./src

pre-commit: format lint

test +ARGS='':
  uv run pytest {{ARGS}}

unit_test:
  uv run pytest --ignore=tests/integration

integration_test:
  uv run pytest --ignore=tests/unit

run +ARGS='':
  uv run dumpster {{ARGS}}
