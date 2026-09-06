---
name: cloud-infrastructure
description: Design and provision secure, observable, recoverable infrastructure with explicit environments, identity, networking, configuration, cost, and rollback. Use only when deployment infrastructure is required.
---

# Cloud Infrastructure

## Workflow

1. Confirm infrastructure is necessary and prefer existing owned or free-first capability.
2. Define environments, identity, network boundaries, secrets, data, and availability targets.
3. Use reviewable infrastructure as code with least privilege and separated state.
4. Validate cost ceilings, observability, backup, rollback, and destruction safeguards.

## Output contract

An infrastructure plan or implementation with controls, cost assumptions, validation, and rollback.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Never provision paid resources, change billing, or perform destructive production actions without explicit approval.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://www.nist.gov/cyberframework) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
