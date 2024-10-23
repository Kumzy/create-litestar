.DEFAULT_GOAL:=help
.PHONY: help install clean update export lint type-check test

.PHONY: help
help: ## Display this help text for Makefile
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: upgrade
upgrade: ## Upgrade all dependencies to the latest stable versions
	@echo "=> Updating all dependencies"
	@uv lock --upgrade
	@echo "=> Dependencies Updated"
	@uv run pre-commit autoupdate
	@echo "=> Updated Pre-commit"

# =============================================================================
# Developer Utils
# =============================================================================
.PHONY: install-uv
install-uv: ## Install latest version of uv
	@curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: install
install: clean ## Install the project, dependencies, and pre-commit for local development
	@uv sync --all-extras --dev
	@echo "=> Install complete!"

clean:  ## Remove generated project files
	@rm -rf .venv/ .*_cache/ .coverage  *.egg-info/ docs/_build

.PHONY: destroy
destroy: ## Destroy the virtual environment
	@rm -rf .venv

.PHONY: lock
lock: ## Rebuild lockfiles from scratch, updating all dependencies
	@uv lock --upgrade

# =============================================================================
# Tests, Linting, Coverage
# =============================================================================
.PHONY: mypy
mypy: ## Run mypy
	@echo "=> Running mypy"
	@uv run mypy run
	@echo "=> mypy complete"

.PHONY: mypy-nocache
mypy-nocache: ## Run Mypy without cache
	@echo "=> Running mypy without a cache"
	@uv run mypy
	@echo "=> mypy complete"

.PHONY: pyright
pyright: ## Run pyright
	@echo "=> Running pyright"
	@uv run pyright
	@echo "=> pyright complete"

.PHONY: type-check
type-check: mypy pyright ## Run all type checking

.PHONY: pre-commit
pre-commit: ## Runs pre-commit hooks; includes ruff formatting and linting, codespell
	@echo "=> Running pre-commit process"
	@uv run pre-commit run --all-files
	@echo "=> Pre-commit complete"

.PHONY: slotscheck
slotscheck: ## Run slotscheck
	@echo "=> Running slotscheck"
	@uv run slotscheck create_litestar/
	@echo "=> slotscheck complete"

.PHONY: lint
lint: pre-commit type-check slotscheck ## Run all linting

.PHONY: coverage
coverage: ## Run the tests and generate coverage report
	@echo "=> Running tests with coverage"
	@uv run pytest tests --cov -n auto
	@uv run coverage html
	@uv run coverage xml
	@echo "=> Coverage report generated"

.PHONY: test
test: ## Run the tests
	@echo "=> Running test cases"
	@uv run pytest tests
	@echo "=> Tests complete"

.PHONY: test-examples
test-examples: ## Run the examples tests
	@uv run pytest docs/examples

.PHONY: test-all
test-all: test test-examples ## Run all tests

.PHONY: check-all
check-all: lint test-all coverage ## Run all linting, tests, and coverage checks
