# codebase-fastapi

## Overview
A scalable and well-structured FastAPI boilerplate for building modern, production-ready APIs. This codebase includes best practices for organizing large projects, dependency injection, async SQLAlchemy support, JWT authentication, background tasks, and more.

## Quick Start

### Using Docker Compose (Recommended)
The easiest way to run the application is using Docker Compose. This will set up all required services (PostgreSQL, Redis) and run the application with proper service orchestration.

```bash
# Start all services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Stop all services
docker-compose down
```

The Docker Compose setup includes:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Automatic database migrations

Services start in the following order:
1. PostgreSQL and Redis (with health checks)
2. Database migrations
3. FastAPI application

### Local Development Setup

#### 1. Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Redis

#### 2. Environment Setup

##### 2.1 Install Dependencies
```bash
# Install all required packages
make install

# Install pre-commit hooks for code quality
make install_precommit
```

#### 3. Database Management

##### 3.1 Generate New Migration
```bash
# Create a new migration with a descriptive name
make DESCRIPTION="your_migration_name" generate_migration
```

##### 3.2 Apply Migrations
```bash
# Apply all pending migrations
make migrate

# Downgrade to base migration if needed
make downgrade
```

#### 4. Running the Application

##### 4.1 Start the Server
```bash
# Run the FastAPI application
make run
```
The application will be available at `http://localhost:8000`

##### 4.2 API Documentation
Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

#### 5. Development Tools

##### 5.1 Running Tests
```bash
# Run the test suite
make test
```

##### 5.2 Code Formatting
```bash
# Format code using isort and ruff
make format
```

## Project Structure
```
codebase-fastapi/
├── app/                    # Application package
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── db/                # Database models and sessions
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── deploy/               # Deployment configurations
├── tests/                # Test suite
├── alembic/              # Database migrations
├── docker-compose.yml    # Docker services configuration
└── requirements-dev.txt  # Development dependencies
```

## Contributing
1. Install pre-commit hooks: `make install_precommit`
2. Create a new branch for your feature
3. Make your changes
4. Run tests: `make test`
5. Format code: `make format`
6. Submit a pull request
