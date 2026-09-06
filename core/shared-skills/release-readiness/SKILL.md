---
name: release-readiness
description: Assess whether a change is ready to release using evidence for functionality, security, performance, operability, migration, rollback, support, and ownership. Use before consequential releases, not as ceremonial approval.
---

# Release Readiness

## Workflow

1. Define release scope, users, blast radius, success signals, and stop conditions.
2. Review required test, security, performance, migration, compatibility, and operational evidence.
3. Verify monitoring, ownership, support, rollback, backup, and communication readiness.
4. Return GO, GO WITH CONDITIONS, NO-GO, or DEFER with one accountable next action.

## Output contract

A release verdict with evidence, conditions, residual risk, and rollback readiness.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not mark GO when a material unresolved issue could invalidate the release outcome.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://sre.google/sre-book/release-engineering/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
