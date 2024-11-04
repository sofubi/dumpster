_default:
  just -l

format:
  uv run black ./src

lint:
  uv run ruff check --fix ./src

pre-commit: format lint

test:
  uv run pytest

run +ARGS='':
  uv run branch-memory {{ARGS}}
