# Generic single-database configuration.

## How to generate migration

1. Make sure to update `config/alembic.ini` with the correct database URL
2. Run `alembic -c config/alembic.ini revision -m "Migration description"`
3. Run `alembic -c config/alembic.ini upgrade head` to migrate the database to the latest version
