---
name: api-design
description: Design evolvable APIs with clear resources, operations, schemas, errors, compatibility rules, authentication boundaries, and machine-readable contracts. Use for service interfaces, not internal function naming alone.
---

# API Design

## Workflow

1. Model consumer jobs, resources, operations, invariants, and authorization boundaries.
2. Define request, response, error, pagination, idempotency, and rate behavior.
3. Publish a machine-readable contract and examples that cover failure cases.
4. Plan compatibility, deprecation, observability, and contract tests before release.

## Output contract

A versioned API contract with semantics, schemas, errors, examples, and tests.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

A schema validates shape, not every semantic or security requirement in the specification.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://spec.openapis.org/oas/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
