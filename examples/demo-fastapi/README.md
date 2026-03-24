# demo-fastapi

CRUD REST API with FastAPI, SQLAlchemy, and SQLite. Manages users and items.

## Description

A RESTful API demonstrating a typical Python project setup with FastAPI:
- Users with name and email
- Items associated with users
- SQLite database with SQLAlchemy ORM
- Tests with pytest and TestClient

## Requirements

- Python 3.11+
- pip

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

```bash
cp .env.example .env
# Edit .env for your environment
```

## Usage

```bash
# Development server
uvicorn src.main:app --reload

# Interactive docs (Swagger)
# http://localhost:8000/docs

# Alternative docs (ReDoc)
# http://localhost:8000/redoc
```

## Tests

```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=src

# A specific test
pytest tests/test_users.py::test_create_user -v
```

## Endpoints

### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List all users |
| GET | /users/{id} | Get user by ID |
| POST | /users | Create user |
| PUT | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user |

### Items

| Method | Path | Description |
|--------|------|-------------|
| GET | /items | List all items |
| GET | /items/{id} | Get item by ID |
| POST | /items | Create item |
| PUT | /items/{id} | Update item |
| DELETE | /items/{id} | Delete item |

## Project Structure

```
src/
├── main.py         # FastAPI app, middlewares, lifespan
├── models.py       # Pydantic schemas + SQLAlchemy models
├── database.py     # DB configuration, session
└── routers/
    ├── users.py    # /users endpoints
    └── items.py    # /items endpoints

tests/
├── conftest.py     # Shared fixtures
├── test_users.py   # User tests
└── test_items.py   # Item tests
```

## Technical Decisions

- **SQLite**: simplicity for demo; switch to PostgreSQL in production
- **TestClient**: synchronous tests without real server overhead
- **Lifespan**: table initialization on app startup
- **Depends()**: dependency injection for the DB session

## Stack

- **FastAPI** 0.111+ — web framework
- **SQLAlchemy** 2.0+ — ORM
- **Pydantic** 2.0+ — data validation
- **uvicorn** — ASGI server
- **pytest** — testing
- **httpx** — HTTP client for tests
