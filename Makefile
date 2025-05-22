# Local use only
SHELL := /bin/bash # Use bash syntax

# Variables
ALEMBIC_CONFIG := config/alembic.ini

# Run the application
run:
	@uvicorn --factory app:create_app \
		--host=0.0.0.0 --port=8000 \
		--log-config=config/log-config.yml

# Install dependencies
install:
	@pip install -r requirements-dev.txt

# Run tests
test:
	@pytest

# Format code
format:
	@isort app && ruff format

# Generate a new database migration
generate_migration:
	alembic -c $(ALEMBIC_CONFIG) revision --autogenerate -m "$(DESCRIPTION)"

# Apply all pending migrations
migrate:
	alembic -c $(ALEMBIC_CONFIG) upgrade head

# Downgrade the database to the base migration
downgrade:
	alembic -c $(ALEMBIC_CONFIG) downgrade base

# Install pre-commit hooks
install_precommit:
	pre-commit install
