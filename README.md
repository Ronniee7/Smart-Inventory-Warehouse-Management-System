# StockPilot

StockPilot is an enterprise-quality Inventory and Warehouse Management System built as a portfolio project to demonstrate professional full-stack engineering practices.

It is an independent portfolio project. It is not affiliated with or endorsed by any employer or client, and it uses only synthetic demonstration data.

## Status

Phase 0 — Repository foundation. The application code is being implemented incrementally, feature by feature, with tests and commits for each change.

## Planned capabilities

- Product catalog and categories
- Supplier management
- Multiple warehouses and storage locations
- Inventory balances and stock movements (receipts, issues, adjustments, transfers)
- Purchase orders and receiving workflows
- Low-stock alerts
- Operational dashboards and reports
- User accounts, organizations, and role-based permissions
- Audit trails and administrative operations

## Technology stack

Backend:
- Python, Django, Django REST Framework
- PostgreSQL
- pytest, pytest-django, Ruff
- OpenAPI documentation

Frontend:
- React, TypeScript (strict mode), Vite
- Vitest, React Testing Library

Infrastructure:
- Git and GitHub
- Docker and Docker Compose
- GitHub Actions
- Redis and Celery (when asynchronous processing is needed)
- Nginx for production deployment

## Architecture

StockPilot uses a modular monolith architecture. Business domains are split into focused Django applications under `backend/apps/`, while the frontend is a separate React/TypeScript application under `frontend/`. See `docs/architecture.md` and `docs/adr/` for details.

## Getting started

Setup instructions will be added as the project is implemented. For now, the repository contains only the foundation structure.

## License

Licensed under the MIT License. See `LICENSE`.
