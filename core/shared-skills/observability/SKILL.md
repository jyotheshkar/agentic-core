---
name: observability
description: Design telemetry that makes system behavior, user impact, failures, and performance diagnosable through correlated traces, metrics, logs, and context. Use for systems that need operational diagnosis or reliability evidence.
---

# Observability

## Workflow

1. Start from user journeys, failure questions, and service objectives.
2. Define events, traces, metrics, logs, context propagation, and ownership at useful cardinality.
3. Protect sensitive data and control telemetry volume and retention.
4. Validate that operators can diagnose representative failures without adding emergency instrumentation.

## Output contract

An observability specification or implementation with signals, queries, alerts, and data controls.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Telemetry volume is not observability. Signals must answer operational questions without leaking sensitive data.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://opentelemetry.io/docs/concepts/signals/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
