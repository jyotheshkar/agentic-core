---
name: backend-engineering
description: Implement server-side domain logic, persistence boundaries, concurrency, authorization, resilience, and operational behavior. Use for backend services and workflows, not when a static or client-only solution is sufficient.
---

# Backend Engineering

## Workflow

1. Define domain invariants, trust boundaries, data ownership, and failure expectations.
2. Choose transaction and consistency semantics before persistence mechanics.
3. Design idempotency, concurrency control, timeouts, retries, and safe error behavior where needed.
4. Add observability and tests around critical paths, authorization, and recovery.

## Output contract

A backend implementation with explicit invariants, interfaces, failure behavior, and tests.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not add a server or distributed service when a simpler local or static solution meets the requirement.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://12factor.net/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
