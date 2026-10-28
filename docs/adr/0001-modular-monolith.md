# ADR 0001: Use a modular monolith

- Status: Accepted
- Date: 2026-10-28

## Context

StockPilot is a portfolio-grade inventory and warehouse management system. The domain is cohesive (products, warehouses, inventory, procurement, reporting) and the team size is one. A distributed system would add operational and cognitive cost without a clear benefit.

## Decision

Build StockPilot as a modular monolith:

- One deployable backend (Django) with domain modules under `backend/apps/`.
- One frontend application (React/TypeScript).
- Clear module boundaries and service layers, but no network calls between modules.

## Consequences

Positive:
- Simpler deployment, testing, and debugging.
- Easier to enforce transactional consistency across domains (especially inventory).
- Faster iteration for a single developer.

Negative:
- All modules scale together.
- Module boundaries must be maintained by convention and tests rather than by network contracts.

## Alternatives considered

- Microservices: rejected as premature; would complicate transactions, deployment, and development for no current benefit.
- Single unstructured Django app: rejected; would harm maintainability and testability.
