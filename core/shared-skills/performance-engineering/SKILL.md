---
name: performance-engineering
description: Define performance objectives, instrument workloads, measure bottlenecks, and validate improvements under representative conditions. Use when latency, throughput, resource use, or scale materially affects the outcome.
---

# Performance Engineering

## Workflow

1. Define user-relevant latency, throughput, resource, and reliability objectives.
2. Build a representative workload and capture a baseline with environment details.
3. Use profiles, traces, metrics, and controlled experiments to localize bottlenecks.
4. Validate improvement, regression risk, capacity limits, and operational cost.

## Output contract

A measured performance report with bottleneck evidence, changes, and validated targets.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not extrapolate synthetic benchmark results to production without workload and environment equivalence.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://web.dev/learn/performance) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
