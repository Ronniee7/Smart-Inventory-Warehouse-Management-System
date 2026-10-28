# Architecture

## Overview

StockPilot is a modular monolith: a single deployable backend application with clearly separated domain modules, plus a separate frontend application.

## Backend layout

- `backend/config/` — project configuration, settings, URLs, WSGI/ASGI.
- `backend/apps/` — Django applications, one per business domain:
  - `core` — shared utilities, base models, health checks.
  - `accounts` — users and authentication.
  - `organizations` — tenants, memberships, roles.
  - `catalog` — products and categories.
  - `warehouses` — warehouses and storage locations.
  - `inventory` — stock movements and balances.
  - `suppliers` — supplier management.
  - `procurement` — purchase orders and receiving.
  - `reporting` — dashboards and reports.
  - `audit` — audit events.

## Design principles

- Business logic lives in service modules, not in views or models.
- Each domain enforces its own invariants; cross-domain calls go through explicit service interfaces.
- Database integrity is enforced with constraints, transactions, and (for inventory) concurrency-safe operations.
- Tenant isolation is enforced on every relevant endpoint.
- All schema changes go through migrations.

## Frontend layout

- `frontend/src/` — React + TypeScript application.
- Feature-based organization under `features/`, shared UI under `components/`, API clients under `api/`.

## Data flow

Clients call the REST API (Django REST Framework). The API validates input, delegates to domain services, and persists through Django ORM to PostgreSQL. Responses are serialized DTOs, never raw models.

## Testing

- Backend: pytest + pytest-django.
- Frontend: Vitest + React Testing Library.
- Database-specific tests run against PostgreSQL in CI.

## Infrastructure

- Docker Compose for local development.
- GitHub Actions for CI.
- Redis and Celery introduced only when asynchronous processing is needed.
