# demo-fastapi

FastAPI CRUD app with SQLite. Users and items resources with full REST endpoints.

## Stack
Python 3.11+ · FastAPI 0.111 · SQLAlchemy 2.0 · SQLite · pytest · ruff · mypy

## Commands
```bash
pip install -r requirements.txt   # install deps
uvicorn src.main:app --reload      # dev server → http://localhost:8000/docs
pytest tests/                      # run tests
make lint                          # ruff check
make typecheck                     # mypy strict
```

## Structure
```
src/main.py       → FastAPI app, CORS, lifespan (creates DB tables)
src/models.py     → Pydantic schemas (UserBase/Create/Response, ItemBase/Create/Response)
                    SQLAlchemy models (UserDB, ItemDB)
src/database.py   → SQLite engine, get_db() Depends, create_all_tables()
src/routers/
  users.py        → GET/POST/PUT/DELETE /users, /users/{id}
  items.py        → GET/POST/PUT/DELETE /items, /items/{id}
tests/
  conftest.py     → TestClient fixture with in-memory DB override
  test_users.py   → CRUD tests for /users
  test_items.py   → CRUD tests for /items
```

## Code Standards
- Type hints everywhere, mypy strict
- Dependency injection via `Depends(get_db)` for DB sessions
- Pydantic v2: use `model_validate()`, `model_dump()`
- Tests use `TestClient` (sync), override DB to SQLite in-memory
- Conventional commits: feat/fix/refactor/test/docs
