.DEFAULT_GOAL:=help
.PHONY: help install clean update export lint type-check test

help: ## Display this help text for Makefile
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install:  clean ## Install project in development mode
	@uv sync --force-reinstall --dev --all-extras

clean:  ## Remove generated project files
	@rm -rf .venv/ .*_cache/ .coverage  *.egg-info/ docs/_build

update:  ## Update project dependencies
	@uv sync --upgrade

export:  ## Export project dependencies
	@uv export --format requirements-txt > requirements.txt

lint:  ## Lint and format codebase
	-@uv run --no-sync ruff check --fix .
	-@uv run ruff format

type-check:  ## Run type checking
	@uv run mypy .

test:  ## Run tests
	@uv run --no-sync pytest .

changelog:	## Generate a changelog
	@uv run git-cliff --config pyproject.toml --output docs/changelog.rst
