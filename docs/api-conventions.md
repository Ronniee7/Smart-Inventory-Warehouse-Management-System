# API Conventions

## Base URL

All API endpoints are prefixed with `/api/v1/`.

## Response format

- Success responses return JSON objects or paginated lists.
- Error responses use a consistent envelope:
  ```json
  { "detail": "...", "code": "..." }
  ```

## Pagination

- Default page size: 25.
- Uses DRF `PageNumberPagination`.
- Query params: `?page=` and `?page_size=`.

## Authentication

- Default permission: deny (no access without authentication).
- Endpoints that must be public (e.g. health checks) explicitly set `AllowAny`.
- Authentication mechanisms are added in the accounts phase.

## Versioning

- URL-based versioning via `/api/v1/`.

## OpenAPI

- Schema: `/api/schema/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Error handling

- Centralized via `apps.core.exceptions.api_exception_handler`.
- Internal errors are not exposed to clients.

## Conventions

- Use plural nouns for resource endpoints.
- Use snake_case for JSON fields.
- Timestamps are ISO 8601 in UTC.
