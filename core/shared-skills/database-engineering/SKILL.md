---
name: database-engineering
description: Design data models, constraints, queries, indexes, migrations, retention, and recovery around domain invariants and workload evidence. Use when persistence behavior materially affects correctness or performance.
---

# Database Engineering

## Workflow

1. Model domain identities, relationships, invariants, lifecycle, and ownership.
2. Enforce critical integrity in the database where practical.
3. Design queries and indexes from measured access patterns, not guesses.
4. Plan reversible migrations, backups, validation, retention, and restore testing.

## Output contract

A data model and migration plan with constraints, query evidence, and recovery controls.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not optimize or denormalize without workload evidence and a measured bottleneck.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://www.postgresql.org/docs/current/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
