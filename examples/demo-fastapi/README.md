# demo-fastapi

REST API CRUD con FastAPI, SQLAlchemy y SQLite. Gestiona usuarios e items.

## Descripción

API RESTful que demuestra un setup típico de proyecto Python con FastAPI:
- Usuarios con nombre y email
- Items asociados a usuarios
- Base de datos SQLite con SQLAlchemy ORM
- Tests con pytest y TestClient

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Variables de entorno

```bash
cp .env.example .env
# Edita .env según tu entorno
```

## Uso

```bash
# Servidor de desarrollo
uvicorn src.main:app --reload

# Documentación interactiva (Swagger)
# http://localhost:8000/docs

# Documentación alternativa (ReDoc)
# http://localhost:8000/redoc
```

## Tests

```bash
# Todos los tests
pytest tests/

# Con cobertura
pytest tests/ --cov=src

# Un test específico
pytest tests/test_users.py::test_create_user -v
```

## Endpoints

### Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /users | Listar todos los usuarios |
| GET | /users/{id} | Obtener usuario por ID |
| POST | /users | Crear usuario |
| PUT | /users/{id} | Actualizar usuario |
| DELETE | /users/{id} | Eliminar usuario |

### Items

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /items | Listar todos los items |
| GET | /items/{id} | Obtener item por ID |
| POST | /items | Crear item |
| PUT | /items/{id} | Actualizar item |
| DELETE | /items/{id} | Eliminar item |

## Estructura del proyecto

```
src/
├── main.py         # App FastAPI, middlewares, lifespan
├── models.py       # Pydantic schemas + SQLAlchemy models
├── database.py     # Configuración DB, sesión
└── routers/
    ├── users.py    # Endpoints /users
    └── items.py    # Endpoints /items

tests/
├── conftest.py     # Fixtures compartidos
├── test_users.py   # Tests de usuarios
└── test_items.py   # Tests de items
```

## Decisiones técnicas

- **SQLite**: simplicidad para demo; cambiar a PostgreSQL en producción
- **TestClient**: tests síncronos sin overhead de servidor real
- **Lifespan**: inicialización de tablas al arrancar la app
- **Depends()**: inyección de dependencia para la sesión de DB

## Stack

- **FastAPI** 0.111+ — framework web
- **SQLAlchemy** 2.0+ — ORM
- **Pydantic** 2.0+ — validación de datos
- **uvicorn** — servidor ASGI
- **pytest** — testing
- **httpx** — cliente HTTP para tests
