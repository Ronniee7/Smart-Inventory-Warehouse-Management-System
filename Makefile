.PHONY: help backend-install backend-run backend-migrate backend-test backend-cov backend-lint backend-format backend-check

help:
	@echo "StockPilot development commands"
	@echo ""
	@echo "Backend:"
	@echo "  make backend-install  - install backend dependencies"
	@echo "  make backend-run      - run Django dev server"
	@echo "  make backend-migrate  - apply database migrations"
	@echo "  make backend-test     - run backend tests"
	@echo "  make backend-cov      - run backend tests with coverage"
	@echo "  make backend-lint     - run Ruff checks"
	@echo "  make backend-format   - apply Ruff formatting"
	@echo "  make backend-check    - run Django system checks"

backend-install:
	cd backend && python -m venv .venv && .venv/Scripts/pip install -e ".[dev]"

backend-run:
	cd backend && python manage.py runserver

backend-migrate:
	cd backend && python manage.py migrate

backend-test:
	cd backend && pytest

backend-cov:
	cd backend && pytest --cov --cov-report=term-missing

backend-lint:
	cd backend && ruff check . && ruff format --check .

backend-format:
	cd backend && ruff format .

backend-check:
	cd backend && python manage.py check && python manage.py makemigrations --check --dry-run
