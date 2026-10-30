# Development Setup

## Prerequisites

- Python 3.12+ (3.14 supported)
- PostgreSQL 15+ (or Docker)
- Git

## Backend

### 1. Create a virtual environment

```bash
cd backend
python -m venv .venv
```

On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -e ".[dev]"
```

### 3. Configure environment

```bash
cp ../.env.example ../.env
```

Edit `.env` and set at least:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL` (or `POSTGRES_*` variables)

### 4. Start PostgreSQL

Using Docker:

```bash
docker run -d --name stockpilot-postgres \
  -e POSTGRES_DB=stockpilot \
  -e POSTGRES_USER=stockpilot \
  -e POSTGRES_PASSWORD=change-me \
  -p 5432:5432 \
  postgres:16
```

Or install PostgreSQL locally and create the database/user matching `.env`.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

API base URL: `http://localhost:8000/api/v1/`

### 7. Run tests

```bash
pytest
```

Tests require a running PostgreSQL instance configured via `DATABASE_URL`.

### 8. Run quality checks

```bash
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Notes

- Do not commit `.env` files.
- The test settings use PostgreSQL. SQLite is not used as a fallback.
- Health endpoint: `GET /api/v1/health/`
- Readiness endpoint: `GET /api/v1/ready/`
- OpenAPI schema: `GET /api/schema/` (in development)
- Swagger UI: `GET /api/docs/` (in development)
