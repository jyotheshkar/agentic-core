---
name: software-architecture
description: Choose and document software boundaries, components, interfaces, data flows, quality attributes, and tradeoffs at the minimum necessary complexity. Use for durable or multi-component systems, not tiny isolated edits.
---

# Software Architecture

## Workflow

1. Start from measurable quality attributes and constraints rather than fashionable technologies.
2. Define boundaries, responsibilities, interfaces, data ownership, and failure domains.
3. Compare the simplest viable options against scale, security, operability, and change cost.
4. Record consequential decisions, rejected alternatives, assumptions, and validation spikes.

## Output contract

An architecture model and decision record with tradeoffs and verification needs.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not introduce distributed infrastructure without a demonstrated requirement that simpler architecture cannot meet.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://www.sei.cmu.edu/our-work/software-architecture/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
